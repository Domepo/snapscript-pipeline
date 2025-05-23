# main.py

import os
import config
import database_operations as db_ops
import ollama_interaction as oi
from thefuzz import fuzz
from thefuzz import process


def find_paragraph_with_fuzzing(source:str, findable_string:str):
    fuzz = process.extract(findable_string, source, limit=1)
    return fuzz[0][0]


def find_section_end_offset(full_text: str, section_to_find: str) -> int | None:
    """
    Findet den End-Offset (Position nach dem letzten Zeichen) des section_to_find im full_text.
    Gibt None zurück, wenn der Abschnitt nicht gefunden wird.
    """
    try:
        fuzzed_text = find_paragraph_with_fuzzing(split_transcript_into_paragraphs(full_text), section_to_find)
        start_index = full_text.index(fuzzed_text) # Nutzt str.index, wirft ValueError wenn nicht gefunden
        return start_index + len(fuzzed_text)
    except ValueError:
        print(f"WARNUNG: Der von Ollama zurückgegebene Abschnitt '{section_to_find[:50]}...' konnte nicht im Haupttranskript gefunden werden.")
        return None


def reconstruct_transcript_with_images(transcript_id: int) -> str | None:
    """
    Rekonstruiert das Transkript mit eingefügten Bild-Platzhaltern.
    """
    full_transcript = db_ops.get_transcript_by_id(transcript_id)
    if not full_transcript:
        print(f"Fehler: Transkript mit ID {transcript_id} nicht gefunden.")
        return None

    markers = db_ops.get_image_markers_for_transcript(transcript_id)
    # Wichtig: Marker in umgekehrter Reihenfolge des Offsets verarbeiten,
    # damit frühere Einfügungen die Offsets späterer (die weiter vorne im Text sind) nicht verändern.
    markers.sort(key=lambda m: m['char_offset'], reverse=True)

    modified_transcript_parts = []
    last_processed_offset = len(full_transcript)

    for marker in markers:
        offset = marker['char_offset']
        image_placeholder = f"\n[BILD: {os.path.basename(marker['image_path'])}]\n" # os.path.basename für kürzeren Pfad

        # Füge den Textteil HINTER dem aktuellen Marker (bis zum letzten verarbeiteten Offset) hinzu
        modified_transcript_parts.append(full_transcript[offset:last_processed_offset])
        # Füge den Bild-Platzhalter hinzu
        modified_transcript_parts.append(image_placeholder)
        # Aktualisiere den letzten verarbeiteten Offset
        last_processed_offset = offset

    # Füge den Textteil VOR dem ersten Marker (oder das gesamte Transkript, wenn keine Marker) hinzu
    modified_transcript_parts.append(full_transcript[:last_processed_offset])

    # Teile in umgekehrter Reihenfolge zusammenfügen (da wir von hinten aufgebaut haben)
    return "".join(reversed(modified_transcript_parts))

def split_transcript_into_paragraphs(transcript_text:str):
    """
    Teilt einen Transkripttext anhand von Zeilenumbrüchen in eine Liste von Absätzen auf.
    """

    paragraphs = [para.strip() for para in transcript_text.strip().split('\n') if para.strip()]
    return paragraphs


if __name__ == "__main__":
    # 1. Datenbank initialisieren
    db_ops.init_db()

    # 2. Das vollständige Transkript (nur einmal oder bei Bedarf)
    #    Lies es aus einer Datei oder definiere es hier.
   

    full_transcript_text = config.FULL_TRANSRIPT_TEXT

    
    # Füge das Transkript hinzu, wenn es noch nicht existiert, oder hole eine bestehende ID.
    # Für dieses Beispiel fügen wir es einfach hinzu. In einer echten Anwendung würdest du
    # vielleicht prüfen, ob es schon da ist, oder es von einer Quelle laden.
    transcript_id = db_ops.add_transcript(full_transcript_text)

    if transcript_id is None:
        print("Konnte Transkript nicht hinzufügen oder abrufen. Breche ab.")
        exit()

    # 3. Bilder und ihre Zuordnung
    # Angenommen, du hast eine Liste von Bildern, die du verarbeiten möchtest
    images_to_process = [
        r"C:\Users\domin\Downloads\3ee2bfc8-cbcb-4373-b77e-92c1e71615fb.png", # Bild zur OBS-Sektion
        # r"pfad/zu/anderem_bild.png", # Z.B. ein Bild zur CCU
        # r"pfad/zu/noch_ein_bild.png" # Z.B. ein Bild zum Videomischer
    ]

    for image_path in images_to_process:
        if not os.path.exists(image_path):
            print(f"FEHLER: Bilddatei '{image_path}' nicht gefunden. Überspringe.")
            continue

        print(f"\nVerarbeite Bild: {image_path}")
        # Relevanten Abschnitt von Ollama holen
        # Wichtig: Immer den VOLLSTÄNDIGEN Originaltext an Ollama senden, damit es den Kontext hat
        matched_section = oi.get_relevant_section_from_ollama(image_path, full_transcript_text)

        if matched_section:
            print(f"  Ollama fand Abschnitt: '{matched_section[:80]}...'")
            # Finde den End-Offset dieses Abschnitts im Originaltranskript
            end_offset = find_section_end_offset(full_transcript_text, matched_section)

            if end_offset is not None:
                db_ops.add_image_marker(transcript_id, image_path, end_offset, matched_section)
            else:
                print(f"  Konnte den von Ollama gefundenen Abschnitt nicht im Originaltext lokalisieren für Bild {image_path}.")
        else:
            print(f"  Konnte keinen relevanten Abschnitt von Ollama für Bild {image_path} erhalten.")

    # 4. Rekonstruiere und gib das Transkript mit Bildmarkern aus
    print("\n--- Rekonstruiertes Transkript mit Bildmarkern ---")
    final_output = reconstruct_transcript_with_images(transcript_id)
    if final_output:
        print(final_output)
    else:
        print("Konnte das Transkript nicht rekonstruieren.")

