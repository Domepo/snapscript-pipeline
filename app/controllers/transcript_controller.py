import os
import config
import collections

from models.transcript import get_transcript_by_id
from models.image_marker import get_image_markers_for_transcript
from models.database import init_db
from models.transcript import add_transcript
from models.transcript_timestamp import get_timestamps
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

def compare_image_text_timestamp(images_path: str, transcript_id: str) -> str:
    """
    Kombiniert ein Text-Transkript mit Bildern aus einem Verzeichnis basierend auf Zeitstempeln.

    Args:
        images_path: Der Pfad zum Verzeichnis mit den Bildern.
                     Die Dateinamen der Bilder müssen die Zeitstempel in Millisekunden sein (z.B. "12345.jpg").
        transcript_id: Die ID des Transkripts, das abgerufen werden soll.

    Returns:
        Einen einzelnen String, der den gesamten Text enthält,
        wobei die Pfade zu den passenden Bildern an den richtigen Stellen eingefügt sind.
    """
    # 1. Hole die Zeitstempel-Intervalle und initialisiere die Datenstrukturen
    intervals = get_timestamps(transcript_id)
    # Ein defaultdict ist praktisch, da wir nicht prüfen müssen, ob ein Schlüssel bereits existiert.
    images_for_interval = collections.defaultdict(list)

    # 2. BILDER VERARBEITEN: Ordne jedes Bild dem richtigen Text-Intervall zu
    print(f"\nDurchsuche Bilder im Verzeichnis: {images_path}")
    for image_file in os.listdir(images_path):
        # Prüfe, ob es sich um eine Bilddatei handelt
        if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        try:
            # Extrahiere den Zeitstempel aus dem Dateinamen
            timestamp = int(os.path.splitext(image_file)[0])
            full_image_path = os.path.join(images_path, image_file)

            # Finde das passende Intervall für das Bild
            for idx, interval in enumerate(intervals):
                start = int(interval['start_timestamp'])
                
                # Bestimme das Ende des Intervalls. Für das letzte Intervall ist das Ende "unendlich".
                # Die Zeit des Bildes muss >= start und < dem start des nächsten Intervalls sein.
                end = float('inf')
                if idx + 1 < len(intervals):
                    end = int(intervals[idx + 1]['start_timestamp'])

                if start <= timestamp < end:
                    print(f"  [Match] Bild '{image_file}' (Timestamp: {timestamp}) gehört zu Intervall {idx} ({start}-{end})")
                    images_for_interval[idx].append(full_image_path)
                    # Da jedes Bild nur zu einem Intervall gehören kann, können wir die innere Schleife abbrechen.
                    break 
        except ValueError:
            # Ignoriere Dateien, deren Namen keine Zahlen sind (z.B. ".DS_Store")
            print(f"  [Warnung] Konnte Timestamp aus '{image_file}' nicht extrahieren. Überspringe.")
            continue
            
    # 3. TEXT ERSTELLEN: Baue den finalen Output zusammen
    print("\nErstelle den finalen Text...")
    output_lines = []
    for idx, interval in enumerate(intervals):
        # Füge die Textzeile hinzu
        output_lines.append(interval['line_text'])

        # Prüfe, ob es für dieses Intervall zugeordnete Bilder gibt
        if idx in images_for_interval:
            # Füge alle gefundenen Bilder hinzu, formatiert zur besseren Lesbarkeit
            for image_path in images_for_interval[idx]:
                output_lines.append(f"[{image_path}]")

    # Verbinde alle Zeilen zu einem einzigen String

    return "\n".join(output_lines)

def images_in_transcript(images_dir: str = "data/cropped", transcript:str = config.FULL_TRANSCRIPT_TEXT) -> None:
    """
    Hauptfunktion, die den gesamten Prozess der Bildverarbeitung und Transkript-Rekonstruktion steuert.
    """ 
   

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
        return final_output
    else:
        print("Konnte das Transkript nicht rekonstruieren.")


