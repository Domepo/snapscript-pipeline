import ollama
import config
from utils.measure_time import measure_time
from utils.token_count import count_tokens
import re
import os


def split_transcript_by_images(full_transcript_text: str) -> list[str]:
    """
    Teilt das Transkript zuverlässig in Abschnitte auf. Ein neuer Abschnitt
    beginnt nach jedem Block von einem oder mehreren aufeinanderfolgenden Bild-Tags.
    """
    # Korrigiertes Pattern (ohne Leerzeichen vor der Dateiendung):
    # - \[ und \] fangen das eckige Tag ein
    # - [^\]]+? erlaubt beliebige Zeichen bis zum schließenden ]
    # - \.(?:jpg|jpeg|png|gif|webp) matcht die Endung
    # - \s* frisst nachfolgende Whitespace-Zeichen
    pattern = r'((?:\[[^\]]+?\.(?:jpe?g|jpeg|png|gif|webp)\]\s*)+)'

    # Split inklusive der Separator-Gruppen
    parts = re.split(pattern, full_transcript_text, flags=re.IGNORECASE)

    chunks: list[str] = []
    # parts = [Text, Bildblock, Text, Bildblock, ..., Text]
    for i in range(0, len(parts) - 1, 2):
        chunk = parts[i] + parts[i+1]
        if chunk.strip():
            chunks.append(chunk.strip())

    # Falls Text nach dem letzten Bildtag kommt
    if len(parts) % 2 == 1 and parts[-1].strip():
        chunks.append(parts[-1].strip())

    print(f"Transkript in {len(chunks)} Abschnitte aufgeteilt.")
    return chunks


@measure_time
def process_chunk_with_ai(chunk_text: str) -> str | None:
    """
    Sendet einen einzelnen Textabschnitt an die KI, um eine Überschrift und formatierten Text zu erhalten.
    """
    prompt = f"""
Du bist ein KI-Assistent zur Textstrukturierung. Deine Aufgabe ist es, für den folgenden Textabschnitt eine passende Überschrift zu erstellen.

Anweisungen:
1.  Erstelle eine prägnante, aussagekräftige Überschrift der Ebene 2 (im Format `## Überschrift`).
2.  Gib den Text des Abschnitts als sauberen Fließtext wieder. Korrigiere offensichtliche Tippfehler und schreibe es lesbarer um, wie ein Volresungsskript.
3.  Behalte den Bild-Tag (z.B. [data/image.jpg]) oder die Bild-Tags am Ende des Textes bei, falls vorhanden.
4.  Gib NUR die Überschrift und den formatierten Text zurück. Beginne direkt mit `##`. Vermeide jede andere Einleitung oder Erklärung.
5.  WICHTIG, DER TEXT SOLL EIN FLIESSTEXT SEIN.

Hier ist der Textabschnitt:
---
{chunk_text}
---
"""
    try:
        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[{'role': 'system', 'content': prompt}],
            options={"num_ctx": config.OLLAMA_NUM_CTX}
        )
        if response and response.get('message', {}).get('content'):
            return response['message']['content'].strip()
        else:
            print("Ollama hat eine leere oder unerwartete Antwort für einen Abschnitt zurückgegeben.")
            return None
    except Exception as e:
        print(f"Fehler bei der Kommunikation mit Ollama für einen Abschnitt: {e}")
        return None

@measure_time
def generate_summary_and_title_with_ai(structured_content: str) -> str | None:
    """
    Erstellt einen Haupttitel und eine Zusammenfassung für das bereits strukturierte Skript.
    """
    prompt = f"""
Du bist ein erfahrener Texter. Du erhältst ein bereits mit Überschriften strukturiertes Vorlesungsskript.

Deine Aufgaben:
1.  Erstelle einen passenden, übergeordneten Titel der Ebene 1 (im Format `# Titel`).
2.  Schreibe eine prägnante Zusammenfassung des gesamten Textes, die etwa 100 Wörter lang ist und die Kernaussagen zusammenfasst.

Gib NUR den Titel und die Zusammenfassung zurück. Formatiere es genau so:
# Dein generierter Titel

Deine generierte Zusammenfassung...

Hier ist das strukturierte Skript:
---
{structured_content}
---
"""
    try:
        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[{'role': 'system', 'content': prompt}],
            options={"num_ctx": config.OLLAMA_NUM_CTX}
        )
        if response and response.get('message', {}).get('content'):
            return response['message']['content'].strip()
        else:
            print("Ollama hat eine leere oder unerwartete Antwort für Titel/Zusammenfassung zurückgegeben.")
            return None
    except Exception as e:
        print(f"Fehler bei der Kommunikation mit Ollama für Titel/Zusammenfassung: {e}")
        return None


def transcript_to_script_iterative(full_transcript_text: str, output_filename: str = "skript_output.md") -> None:
    """
    Verarbeitet ein Transkript iterativ, indem es in Abschnitte aufgeteilt
    und jeder Abschnitt einzeln an eine KI gesendet wird. Schreibt das Ergebnis in eine Datei.
    """
    # 1. Transkript in Abschnitte aufteilen
    chunks = split_transcript_by_images(full_transcript_text)
    
    if not chunks:
        print("Keine verarbeitbaren Abschnitte im Transkript gefunden.")
        return

    # 2. Jeden Abschnitt einzeln verarbeiten
    processed_parts = []
    for i, chunk in enumerate(chunks):
        print(f"Verarbeite Abschnitt {i+1}/{len(chunks)}...")
        # Die Bild-Tags können lange Pfade haben, wir zeigen nur das Ende zur Identifikation
        end_of_chunk = chunk.strip()[-40:].replace('\n', ' ')
        print(f"  -> Inhalt endet mit: '...{end_of_chunk}'")
        
        # Zähle die Tokens für den Abschnitt und passe die Konfiguration an
        config.OLLAMA_NUM_CTX = count_tokens(chunk)

        processed_chunk = process_chunk_with_ai(chunk)
        if processed_chunk:
            processed_parts.append(processed_chunk)
        else:
            # Falls ein Aufruf fehlschlägt, nehmen wir den Originaltext, um nichts zu verlieren.
            print(f"  -> KI-Verarbeitung für Abschnitt {i+1} fehlgeschlagen. Verwende Originaltext.")
            processed_parts.append(f"## Unbenannter Abschnitt {i+1}\n\n{chunk}")

    # 3. Alle verarbeiteten Teile zu einem großen Text zusammenfügen
    structured_content = "\n\n".join(processed_parts)
    
    # 4. Titel und Zusammenfassung für den Gesamttext generieren
    print("\nGeneriere finalen Titel und Zusammenfassung für das gesamte Skript...")

    # Zähle die Tokens für den Abschnitt und passe die Konfiguration an
    config.OLLAMA_NUM_CTX = count_tokens(structured_content)

    header_part = generate_summary_and_title_with_ai(structured_content)
    
    if not header_part:
        print("Konnte keinen Titel und keine Zusammenfassung erstellen. Das Skript wird ohne Header gespeichert.")
        header_part = "# Unbenanntes Skript\n\n(Zusammenfassung konnte nicht generiert werden.)"

    # 5. Alles kombinieren und in eine Datei schreiben
    final_script = f"{header_part}\n\n{structured_content}"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(final_script)
        print(f"\n✅ Skript erfolgreich in die Datei '{output_filename}' geschrieben.")
        print(f"   Pfad: {os.path.abspath(output_filename)}")
    except IOError as e:
        print(f"\n❌ Fehler beim Schreiben der Datei: {e}")