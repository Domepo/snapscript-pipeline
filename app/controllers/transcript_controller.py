import os
import config
from models.transcript import get_transcript_by_id
from models.image_marker import get_image_markers_for_transcript
from models.database import init_db
from models.transcript import add_transcript
from models.image_marker import add_image_marker
from services.ollama_service import get_relevant_section
from utils.text_utils import find_section_end_offset 


def reconstruct_transcript_with_images(transcript_id: int) -> str | None:
    full_text = get_transcript_by_id(transcript_id)
    if not full_text:
        return None

    markers = get_image_markers_for_transcript(transcript_id)
    markers.sort(key=lambda m: m['char_offset'], reverse=True)

    parts = []
    last_offset = len(full_text)

    for marker in markers:
        offset = marker['char_offset']
        # placeholder = f"\n[BILD: {os.path.basename(marker['image_path'])}]\n"
        image_path_normalized = marker['image_path'].replace("\\", "/")
        placeholder = f"\n[{image_path_normalized}]\n"

        parts.append(full_text[offset:last_offset])
        parts.append(placeholder)
        last_offset = offset

    parts.append(full_text[:last_offset])
    return "".join(reversed(parts))

def images_in_transcript(images_dir: str = "data/cropped", transcript:str = config.FULL_TRANSCRIPT_TEXT) -> None:
    """
    Hauptfunktion, die den gesamten Prozess der Bildverarbeitung und Transkript-Rekonstruktion steuert.
    """ 

    init_db()
   

    full_transcript_text = transcript

    
    # Füge das Transkript hinzu, wenn es noch nicht existiert, oder hole eine bestehende ID.
    # Für dieses Beispiel fügen wir es einfach hinzu. In einer echten Anwendung würdest du
    # vielleicht prüfen, ob es schon da ist, oder es von einer Quelle laden.
    transcript_id = add_transcript(full_transcript_text)

    if transcript_id is None:
        print("Konnte Transkript nicht hinzufügen oder abrufen. Breche ab.")
        exit()

    # 3. Bilder und ihre Zuordnung
    # Angenommen, du hast eine Liste von Bildern, die du verarbeiten möchtest

    images_to_process = [
        os.path.join(images_dir, f)
        for f in os.listdir(images_dir)
        if os.path.isfile(os.path.join(images_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]

    for image_path in images_to_process:
        if not os.path.exists(image_path):
            print(f"FEHLER: Bilddatei '{image_path}' nicht gefunden. Überspringe.")
            continue

        print(f"\nVerarbeite Bild: {image_path}")
        # Relevanten Abschnitt von Ollama holen
        # Wichtig: Immer den VOLLSTÄNDIGEN Originaltext an Ollama senden, damit es den Kontext hat
        matched_section = get_relevant_section(image_path, full_transcript_text)

        if matched_section:
            print(f"  Ollama fand Abschnitt: '{matched_section[:80]}...'")
            # Finde den End-Offset dieses Abschnitts im Originaltranskript
            end_offset = find_section_end_offset(full_transcript_text, matched_section)

            if end_offset is not None:
                add_image_marker(transcript_id, image_path, end_offset, matched_section)
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


