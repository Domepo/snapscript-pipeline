import re
# === Importiere deine Builder- und Compiler-Funktionen ===
from services.typst.builders import (
    build_first_person,
    build_heading,
    build_section,
    build_sys_inputs
)
from services.typst.compiler import compile_document
import typst # Für typst.TypstCompileError in der Fehlerbehandlung


# === PARSER-LOGIK (MIT KORRIGIERTER BILDERKENNUNG) ===
def parse_markdown_to_document_parts(markdown_text: str):
    lines = markdown_text.strip().split('\n')

    doc_title = "Standardtitel"
    doc_abstract_content_elements = [] 
    parsed_sections_data = [] 

    current_section_title = None
    current_section_content_elements = []
    
    state = 0 
    text_buffer = [] 

    def flush_text_buffer_to_content(buffer: list, content_list: list):
        if buffer:
            processed_value = ""
            temp_para = []
            for line_in_buffer in buffer:
                stripped_line = line_in_buffer.strip()
                if not stripped_line:
                    if temp_para:
                        processed_value += "\n".join(l.strip() for l in temp_para) + "\n\n"
                        temp_para = []
                else:
                    temp_para.append(line_in_buffer)
            if temp_para:
                 processed_value += "\n".join(l.strip() for l in temp_para)
            
            value = processed_value.strip()
            if value:
                content_list.append({"type": "text", "value": value})
            buffer.clear()

    def finalize_current_section():
        nonlocal current_section_title, current_section_content_elements, text_buffer
        flush_text_buffer_to_content(text_buffer, current_section_content_elements)
        if current_section_title and current_section_content_elements:
            parsed_sections_data.append({
                "name": current_section_title,
                "content": list(current_section_content_elements) 
            })
        current_section_content_elements.clear()
        current_section_title = None

    for line_original in lines:
        line = line_original.strip()

        h1_match = re.match(r"^#\s+(.*)", line)
        h2_match = re.match(r"^##\s+(.*)", line)
        # KORRIGIERTES/PRÄZISERES Regex für Bilder:
        img_match = re.match(r"^\[(data/(cropped/[^\]]+))|(cropped/[^\]]+)|([^\]]+)\]$", line)


        if h1_match:
            if state > 0:
                finalize_current_section()
                flush_text_buffer_to_content(text_buffer, doc_abstract_content_elements)
            doc_title = h1_match.group(1).strip()
            state = 1 
            text_buffer.clear()
        
        elif h2_match:
            if state == 1:
                flush_text_buffer_to_content(text_buffer, doc_abstract_content_elements)
            finalize_current_section()
            current_section_title = h2_match.group(1).strip()
            state = 2
            text_buffer.clear()

        elif img_match:
            image_path_in_dict = ""
            
            path_data_cropped_full = img_match.group(1)     # z.B. "data/cropped/img.jpg" oder None
            path_data_cropped_relative = img_match.group(2) # z.B. "cropped/img.jpg" oder None
            path_cropped_only = img_match.group(3)          # z.B. "cropped/img.jpg" oder None
            path_other = img_match.group(4)                 # z.B. "images/foo.png" oder None
            
            if path_data_cropped_relative: # Priorität: [data/cropped/...]
                image_path_in_dict = "/" + path_data_cropped_relative.lstrip('/')
            elif path_cropped_only:    # Nächste Priorität: [cropped/...]
                image_path_in_dict = "/" + path_cropped_only.lstrip('/')
            elif path_other:      # Fallback: Anderes Format, z.B. [images/foo.png]
                image_path_in_dict = "/" + path_other.lstrip('/')
            else:
                # Sollte nicht passieren, wenn Regex matched, aber als Sicherheitsnetz
                raw_path_content = line.strip()[1:-1] # Inhalt der Klammern
                image_path_in_dict = "/" + raw_path_content.lstrip('/')
                print(f"WARNUNG: Bildpfad aus '{line}' konnte nicht standardmäßig extrahiert werden, verwende '{image_path_in_dict}'.")

            image_filename = image_path_in_dict.split('/')[-1]
            image_element = {
                "type": "image",
                "path": image_path_in_dict,
                "caption": f"Abbildung: {image_filename}", 
                "width": 0.5 
            }

            if state == 0: 
                print(f"Hinweis: Bild '{image_filename}' ({image_path_in_dict}) vor Hauptüberschrift. Erstelle implizite Sektion 'Einleitung'.")
                finalize_current_section()
                flush_text_buffer_to_content(text_buffer, current_section_content_elements)
                current_section_title = "Einleitung" 
                current_section_content_elements.append(image_element)
                state = 2
            elif state == 1: 
                flush_text_buffer_to_content(text_buffer, doc_abstract_content_elements)
                print(f"Hinweis: Bild '{image_filename}' ({image_path_in_dict}) im Abstract-Bereich. Wird erster/impliziter Sektion zugeordnet.")
                if not current_section_title and not parsed_sections_data: 
                    current_section_title = "Einleitung"
                state = 2
                current_section_content_elements.append(image_element)
            elif state == 2: 
                flush_text_buffer_to_content(text_buffer, current_section_content_elements)
                current_section_content_elements.append(image_element)
        
        elif line_original.strip() == "" : 
            if (state == 1 or state == 2) and text_buffer: 
                 text_buffer.append("")
        
        elif line_original.strip():
            if state == 0:
                text_buffer.append(line_original)
            elif state == 1:
                text_buffer.append(line_original)
            elif state == 2:
                text_buffer.append(line_original)
    
    if state == 0 and text_buffer: 
        if doc_title == "Standardtitel": doc_title = "Unbenanntes Dokument"
        current_section_title = "Einleitung"
        flush_text_buffer_to_content(text_buffer, current_section_content_elements)

    if state == 1:
        flush_text_buffer_to_content(text_buffer, doc_abstract_content_elements)
    
    finalize_current_section()

    final_abstract_str = "\n\n".join(
        item['value'] for item in doc_abstract_content_elements if item['type'] == 'text'
    ).strip()

    if not final_abstract_str and state == 0 and not doc_abstract_content_elements and text_buffer:
        temp_abstract_elements = []
        flush_text_buffer_to_content(text_buffer, temp_abstract_elements)
        final_abstract_str = "\n\n".join(
            item['value'] for item in temp_abstract_elements if item['type'] == 'text'
        ).strip()
        if final_abstract_str and doc_title == "Standardtitel":
            doc_title = "Unbenanntes Dokument"

    final_built_sections = []
    for sec_data in parsed_sections_data:
        final_built_sections.append(build_section(name=sec_data["name"], content=sec_data["content"]))
        
    return doc_title, final_abstract_str, final_built_sections
# === ENDE PARSER-LOGIK ===


# Dein Markdown-Text
# markdown_input = """
# # Livestream-Technik

# Das ist eine ZUsammenfassung der Vorlesung, die ich heute gehalten habe.
# Hier kommt die Zusammenfassung deiner Vorlesung/dokument. Beschreibe knapp, worum es geht.  

# ## Test
# Herzlich willkommen zur heutigen Vorlesung. Heute soll es um Livestream-Technik gehen. Da unterteilen wir verschiedene Bereiche: den Bildbereich, den Videobereich, die Lichtbereiche – wie das alles ausgeleuchtet werden muss. Das werden wir in einem schönen Diagramm haben. Das sind die verschiedenen Ebenen. Wir haben natürlich ganz oben das, was man sieht. Das, was man sieht, ist ein Auge. Dann haben wir hier die Kabel und die ganzen Verbindungen und unten haben wir dann Software.

# ## OBS: Das Tor zum guten Livestream

# Wichtig ist auch, dass – das ist ein Zitat von mir – OBS das Tor zum guten Livestream ist.

# ## Kameras und Anschlüsse

# Dann würde ich einmal gerne mit den Kameras anfangen. Genau, hier symbolisch eine Kamera. Also, wir haben verschiedene Möglichkeiten: HDMI-betriebene Kameras, SDI-Kameras, Glasfaser und auch IP, also Ethernet-Kameras. Bei HDMI ist es so, dass wir nur kurze Strecken, aber hohe Bandbreite haben. SDI haben wir sehr lange Strecken und eine etwas niedrigere Bandbreite. Glasfaser hat dann gigantische Strecken und gigantische Bandbreite. Und bei IP-Ethernet haben wir – das ist das Ding – dass man vielleicht noch mit ein paar Latenzen zu kämpfen hat, aber seit dem neuen IB2110-Standard von MacMagic ist das auch schon nicht mehr so wichtig.

# [data/cropped/crop1camera4.jpg]

# ## Kamera-Aufbau: Buddy, Bayonett und Objektive

# Genau, wie ist eine Kamera aufgebaut? Wir haben zum einen, das nennt man Buddy. Dieses Buddy ist dann die Kamera mit einem gewissen Bayonet. Und das ist hier das Bayonet. Bayonet. Und da gibt es verschiedene Optionen. Man hat EF-Bayonets, zum Beispiel von Canon. Also hier kann ich hinschreiben: Canon ist gleich EF. Fujifilm hat mehrere. Eins davon ist die XF-Serie. Aber das ist einfach nur der Verschluss für das Objektiv, was dann hier hinkommt. Hier ist das Objektiv.

# [data/cropped/crop_0_camera-7.jpg]
# """


def main(markdown_input: str):
    # === 1. Metadaten definieren (bleibt meist manuell) ===
    first_person_dict = build_first_person(
        name="Prof. Dr. rer. nat. Vorname Nachname",
        uni="Beispiel-Universität",
        email="email@beispiel.de",
        phone="+49 1234 567890"
    )

    # === Parser aufrufen ===
    parsed_title, parsed_abstract_str, parsed_sections_list_of_dicts = \
        parse_markdown_to_document_parts(markdown_input)

    # === Heading mit geparsten Daten erstellen ===
    heading_dict = build_heading(
        title=parsed_title,
        abstract=parsed_abstract_str,
        keywords=["Livestream", "Technik", "OBS", "Kameras"], 
        date="4 Juni, 2025" 
    )

    # === 2. Abschnitte (Sections) verwenden die geparsten Daten ===
    sections_list_of_dicts = parsed_sections_list_of_dicts
    
    # === 3. Sys-Inputs zusammenbauen ===
    sys_inputs_with_json_strings = build_sys_inputs(
        first_person=first_person_dict,
        heading=heading_dict,
        sections=sections_list_of_dicts 
    )

    # === 4. Dokument kompilieren ===
    typst_input_path = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data/typst/lecture.typ"
    pdf_output_path   = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data/typst/lecture.pdf"
    root_directory    = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data"

    print("Starte Typst-Kompilierung...")
    print(f"  Typst Input: {typst_input_path}")
    print(f"  PDF Output: {pdf_output_path}")
    print(f"  Root Directory: {root_directory}")
    
    # Optional: Detaillierte Ausgabe der generierten Bildpfade zur Überprüfung
    print("\n  --- Generierte Bildpfade in Sections ---")
    for i, section_dict in enumerate(sections_list_of_dicts):
        print(f"  Section {i+1}: {section_dict.get('name')}")
        for content_item in section_dict.get('content', []):
            if content_item.get('type') == 'image':
                print(f"    Bildpfad: {content_item.get('path')}")
    print("  --- Ende Bildpfade ---\n")


    try:
        compile_document(
            sys_inputs=sys_inputs_with_json_strings,
            typst_input=typst_input_path,
            pdf_output=pdf_output_path,
            root_path=root_directory
        )
        print(f"Kompilierung erfolgreich! PDF erstellt unter: {pdf_output_path}")
    except FileNotFoundError as e:
        print(f"FEHLER bei der Kompilierung: Datei nicht gefunden. Überprüfe die Pfade.")
        print(f"  Fehlermeldung: {e}")
        print(f"  Stelle sicher, dass die Typst-Datei existiert: {typst_input_path}")
        print(f"  Stelle sicher, dass das Wurzelverzeichnis existiert: {root_directory}")
    except typst.TypstCompileError as e: 
        print(f"FEHLER bei der Typst-Kompilierung:")
        print(e) 
    except Exception as e:
        print(f"Ein unerwarteter FEHLER ist während der Kompilierung aufgetreten: {e}")
        print(f"  Typ des Fehlers: {type(e)}")

    print("\nSkript-Ausführung beendet.")