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
from utils.measure_time import measure_time

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

@measure_time
def compare_image_text_timestamp(images_path: str, transcript_id: str,  transcript_with_image_path:str = "data/transcript/transcript_with_images.txt") -> str:
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

    # Sortiere die Bilder nach Dateinamen, die als Zeitstempel fungieren
    all_images = [f for f in os.listdir(images_path) if f.lower().endswith(('.png','.jpg','.jpeg'))]

    all_images_sorted = sorted(
        all_images,
        key=lambda fn: int(os.path.splitext(fn)[0])  # Dateiname ohne Extension → int
    )


    for image_file in all_images_sorted:
        # Prüfe, ob es sich um eine Bilddatei handelt
        if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
    
        # Extrahiere den Zeitstempel aus dem Dateinamen
        base, ext = os.path.splitext(image_file)
        timestamp = int(base) 


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
                posix_path = image_path.replace(os.path.sep, "/")
                output_lines.append(f"[{posix_path}]")

    # Verbinde alle Zeilen zu einem einzigen String
    # print("\n".join(output_lines))
    with open(transcript_with_image_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print("Fertig – siehe transcript_with_images.txt")
    print(f"Anzahl Zeilen in output_lines: {len(output_lines)}")
    return "\n".join(output_lines)

