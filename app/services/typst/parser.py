# services/typst/parser.py

import re
from typing import List, Dict

def parse_markdown(text: str) -> Dict:
    """
    Parst ein Markdown-ähnliches Dokument mit:
      #  Titel
      (Text → Abstract)
      ## Abschnittsüberschrift
      (Text + [bildpfad] + Text)
      ## Nächste Abschnittsüberschrift
      ...
    Gibt zurück:
    {
      "title": "Dokumenttitel",
      "abstract": "Textabsatz vor dem ersten Abschnitt",
      "sections": [
        {
          "name": "Abschnittsname",
          "content": [
            {"type": "text", "value": "..."},
            {"type": "image", "path": "...", "caption": "", "width": 0.5},
            ...
          ]
        },
        ...
      ]
    }
    """

    lines = text.splitlines()
    title = ""
    abstract_buffer: List[str] = []
    sections: List[Dict] = []

    current_section_name = None
    current_content: List[Dict] = []
    section_text_buffer: List[str] = []

    in_first_section = False
    final_abstract = ""

    # Pattern für Bildzeilen: Eine komplette Zeile in eckigen Klammern, z.B. "[pfad/zum/bild.jpg]"
    image_pattern = re.compile(r'^\[([^\]]+)\]\s*$')

    def flush_text_buffer_to_list(buffer: List[str], out_list: List[Dict]):
        """
        Hilfsfunktion: Sammelt alle Zeilen in `buffer`, fasst sie zu einem einzigen Text-Element zusammen
        und hängt es als {"type": "text", "value": ...} an `out_list` an. Leert anschließend `buffer`.
        """
        s = "\n".join([l for l in buffer if l.strip() != ""]).strip()
        if s:
            out_list.append({"type": "text", "value": s})
        buffer.clear()

    for raw_line in lines:
        line = raw_line.rstrip()

        # 1) Titel-Zeile: "# Livestream-Technik: Ein Überblick"
        if not title and line.startswith("# "):
            title = line[2:].strip()
            continue

        # 2) Abschnitts-Überschrift: "## Abschnittsname"
        if line.startswith("## "):
            # Wenn wir das erste Mal in einen Abschnitt wechseln:
            if not in_first_section:
                in_first_section = True
                # Flush aller bisher gesammelten Abstract-Zeilen zu einem einzigen Text
                final_abstract = "\n".join([l for l in abstract_buffer if l.strip() != ""]).strip()
            else:
                # Bevor wir den alten Abschnitt speichern, alles im section_text_buffer sichern
                flush_text_buffer_to_list(section_text_buffer, current_content)
                # Alten Abschnitt abschließen
                sections.append({
                    "name": current_section_name,
                    "content": current_content.copy()
                })
                current_content.clear()

            # Setze den neuen Abschnittsnamen
            current_section_name = line[3:].strip()
            section_text_buffer.clear()
            continue

        # 3) Bild-Zeile? (z. B. "[data/cropped/crop1camera4.jpg]")
        m = image_pattern.match(line)
        if m:
            img_path = m.group(1).strip()
            if in_first_section:
                # Flush vorhandenen Text-Puffer
                flush_text_buffer_to_list(section_text_buffer, current_content)
                current_content.append({
                    "type": "image",
                    "path": img_path,
                    "caption": "",
                    "width": 0.5
                })
            else:
                # Falls das Bild in den Abstract fällt, schieben wir die Zeile einfach in den abstract_buffer
                abstract_buffer.append(line)
            continue

        # 4) Normale Text-Zeile:
        if in_first_section:
            section_text_buffer.append(line)
        else:
            abstract_buffer.append(line)

    # Nach Ende der Schleife: letzen Abschnitt (sofern vorhanden) flushen / speichern
    if not in_first_section:
        # Es gab keine "##"-Abschnitte – alles ist Abstract
        final_abstract = "\n".join([l for l in abstract_buffer if l.strip() != ""]).strip()
    else:
        # Flush für den letzten Abschnitt
        flush_text_buffer_to_list(section_text_buffer, current_content)
        if current_section_name is not None:
            sections.append({
                "name": current_section_name,
                "content": current_content.copy()
            })

    return {
        "title": title,
        "abstract": final_abstract,
        "sections": sections
    }


# Falls du die Funktion direkt testen möchtest, kannst du in dieser Datei z.B. am Ende folgenden Block hinzufügen:
if __name__ == "__main__":
    sample = """# Livestream-Technik: Ein Überblick

    Herzlich willkommen zur heutigen Vorlesung. Heute soll es um Livestream-Technik gehen. Da unterteilen wir verschiedene Bereiche: den Bildbereich, den Videobereich, die Lichtbereiche – wie das alles ausgeleuchtet werden muss. Das werden wir in einem schönen Diagramm haben. Das sind die verschiedenen Ebenen. Wir haben natürlich ganz oben das, was man sieht. Das, was man sieht, ist ein Auge. Dann haben wir hier die Kabel und die ganzen Verbindungen und unten haben wir dann Software.

    ## OBS: Das Tor zum guten Livestream

    Wichtig ist auch, dass – das ist ein Zitat von mir – OBS das Tor zum guten Livestream ist.

    ## Kameras und Anschlüsse

    Dann würde ich einmal gerne mit den Kameras anfangen. Genau, hier symbolisch eine Kamera. Also, wir haben verschiedene Möglichkeiten: HDMI-betriebene Kameras, SDI-Kameras, Glasfaser und auch IP, also Ethernet-Kameras. Bei HDMI ist es so, dass wir nur kurze Strecken, aber hohe Bandbreite haben. SDI haben wir sehr lange Strecken und eine etwas niedrigere Bandbreite. Glasfaser hat dann gigantische Strecken und gigantische Bandbreite. Und bei IP-Ethernet haben wir – das ist das Ding – dass man vielleicht noch mit ein paar Latenzen zu kämpfen hat, aber seit dem neuen IB2110-Standard von MacMagic ist das auch schon nicht mehr so wichtig.

    [data/cropped/crop1camera4.jpg]

    ## Kamera-Aufbau: Buddy, Bayonett und Objektive

    Genau, wie ist eine Kamera aufgebaut? Wir haben zum einen, das nennt man Buddy. Dieses Buddy ist dann die Kamera mit einem gewissen Bayonet. Und das ist hier das Bayonet. Bayonet. Und da gibt es verschiedene Optionen. Man hat EF-Bayonets, zum Beispiel von Canon. Also hier kann ich hinschreiben: Canon ist gleich EF. Fujifilm hat mehrere. Eins davon ist die XF-Serie. Aber das ist einfach nur der Verschluss für das Objektiv, was dann hier hinkommt. Hier ist das Objektiv.

    [data/cropped/crop_0_camera-7.jpg]
    """
    result = parse_markdown(sample)
    import pprint
    pprint.pprint(result)
