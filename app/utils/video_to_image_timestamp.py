from pathlib import Path
from datetime import datetime
from utils.image_distance import compare_successive_images
from utils.compare_images import absolute_diff_compare
from utils.measure_time import measure_time
from collections import deque

import cv2
import numpy as np
from PIL import Image

def get_image_edges(img: Image.Image):
    """
    Berechnet die Anzahl an Kanten im Bild.
    """
    img_gray = np.array(img.convert("L"))
    edges = cv2.Canny(img_gray, 100, 200)
    num_edges = np.sum(edges > 0)
    return num_edges


def detect_fade(frames):
    """
    Detects a fade-out effect in a sequence of video frames based on grayscale brightness analysis.

    Steps:
    1. Converts each frame to grayscale and calculates the average brightness.
    2. Uses the last 10 brightness values to check for a decreasing trend (indicating a fade-out).
    3. If a fade-out is detected:
        - Calculates the frame-to-frame differences in brightness across the entire sequence.
        - Traverses the differences in reverse to find where the fade likely started.
        - Identifies the index of the last 'unfaded' frame, based on a small brightness change threshold.
    4. Returns the unfaded frame at the detected index.

    Parameters:
    - frames (list of PIL.Image): The full list of video frames to analyze.

    Returns:
    - PIL.Image or None: The last unfaded frame before the fade-out began,
      or None if no fade-out is detected.
    """
    # WEnn der vorherige oder der nachfoglenden mehr kanten hat wird das genommen
    difference_threshold = 4
    # Convert all frames to grayscale brightness values
    gray_means_full = [np.array(f.convert("L")).mean() for f in frames]

    # Only look at the last 10 values to detect a fade
    gray_means_recent = gray_means_full[-10:]

    if gray_means_recent == sorted(gray_means_recent, reverse=True):
        print("FADE ERKANNT")

        # Now analyze brightness differences across the full list
        difference = np.diff(gray_means_full)
        reversed_difference = np.flip(difference)

        for idx, diff in enumerate(reversed_difference):
            abs_diff = abs(diff)

            if abs_diff < difference_threshold:
                number_of_unfaded_image = len(reversed_difference)-idx
                print(f"Number of unfaded image: {number_of_unfaded_image}")
                return frames[number_of_unfaded_image]



@measure_time
def extract_frames_rename_by_timestamp(
    video_path: str,
    output_dir: str = "frames",
    image_format: str = "jpg",
    ts_pattern: str = "%Y%m%d_%H%M%S_%f",   # Dateinamen-Format
    recording_start: datetime | None = None # absoluter Startzeitpunkt
) -> None:
    """
    Liest ein Video frame-weise ein, speichert Bilder, die sich deutlich vom vorherigen unterscheiden,
    und benennt sie nach Timestamp. Bilder werden zunächst gesammelt und am Ende auf Dopplungen geprüft.
    """
    frame_set = deque(maxlen=200)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Konnte Video '{video_path}' nicht öffnen.")

    fps = cap.get(cv2.CAP_PROP_FPS)
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if recording_start is None:
        recording_start = datetime.now().replace(microsecond=0)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    previous_img = None

    # Hier sammeln wir die Kandidatenbilder
    candidate_images = []
    candidate_filenames = []

    print("Phase 1: Kandidatenbilder aus Video extrahieren...")
    for idx in range(total_frames):
        
        ok, frame_bgr = cap.read()
        if not ok:
            break

        elapsed_ms = int((idx / fps) * 1000)
        ts_str = f"{elapsed_ms:010d}"
        file_name = out_path / f"{ts_str}.{image_format}"

        img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))

        frame_set.append(img)

        if previous_img is None:
            previous_img = img
            continue 

        image_difference = compare_successive_images(previous_img, img)


        # Speichere das unfaded image
        check_brightness = np.array(img.convert("L")).mean()
        if check_brightness < 1:
            print(f"Füge Unfaded-Kandidat {file_name} hinzu")
            unfaded_image = detect_fade(frame_set)
            candidate_images.append(unfaded_image.copy()) 
            candidate_filenames.append(file_name)

        print(f"ID: {idx}, Difference {image_difference}, Edges {get_image_edges(previous_img)}, Test: {check_brightness}")
        if image_difference > 25 and get_image_edges(previous_img) > 5000:

            print(f"Änderung nach Frame {idx-1} erkannt. Füge Kandidat hinzu.")
            
            # Wichtig: Speichere das *vorherige* Bild mit dem *vorherigen* Dateinamen
            prev_elapsed_ms = int(((idx - 1) / fps) * 1000)
            prev_ts_str = f"{prev_elapsed_ms:010d}"
            prev_file_name = out_path / f"{prev_ts_str}.{image_format}"

            candidate_images.append(previous_img.copy())  # .copy() ist hier entscheidend!
            candidate_filenames.append(prev_file_name)

        previous_img = img


    cap.release()
    print(f"Phase 1 abgeschlossen. {len(candidate_images)} Kandidaten gefunden.")

    # --- KORRIGIERTER TEIL ---
    print("\nPhase 2: Dopplungen prüfen und finale Bilder speichern...")

    if not candidate_images:
        print("Keine relevanten Bilder zum Speichern gefunden.")
        return

    FORMAT_MAP = {
        "jpg":  "JPEG", "jpeg": "JPEG",
        "png":  "PNG",  "tif":  "TIFF",
    }
    pillow_fmt = FORMAT_MAP.get(image_format.lower(), "JPEG")
    
    # Wir erstellen eine neue Liste mit den Bildern, die wir wirklich behalten wollen.
    final_images_to_save = []
    
    # Das erste Bild der Kandidatenliste wird immer behalten.
    last_kept_image = candidate_images[0]
    final_images_to_save.append((candidate_filenames[0], last_kept_image))

    # Gehe durch die restlichen Kandidaten und vergleiche sie mit dem letzten Bild, das wir behalten haben.
    for i in range(1, len(candidate_images)):
        current_img = candidate_images[i]
        current_filename = candidate_filenames[i]

        # Prüfe, ob das aktuelle Bild eine exakte Kopie/Teilmenge des letzten behaltenen Bildes ist.
        # Deine Funktion prüft, ob A in B enthalten ist. Wir wollen also prüfen:
        # Ist das `current_img` im `last_kept_image` enthalten? (z.B. ein Menü verschwindet)
        # Oder ist das `last_kept_image` im `current_img` enthalten? (z.B. ein Menü erscheint)
        # Wenn beides nicht der Fall ist, ist es ein wirklich neues Bild.

        if absolute_diff_compare(last_kept_image, current_img):
            #Bild data\tmp\0000197166.jpg ist ein Duplikat/Teilbild von 0000059166.jpg. Überspringe.
            print(f"Bild {current_filename} ist ein Duplikat/Teilbild von {final_images_to_save[-1][0].name}.")
            final_images_to_save.pop(-1)
            final_images_to_save.append((current_filename, current_img))
            print("-> Vorheriges wird nicht gespeichert, da es ein Duplikat ist.")
            
        else:
            # Kein Duplikat -> behalten und als neue Referenz setzen.
            print(f"Bild {current_filename.name} ist neu. Wird behalten.")
            last_kept_image = current_img
            final_images_to_save.append((current_filename, current_img))

    # Speichere alle Bilder, die wir am Ende behalten wollen.

    """
    Wir entfernen das allererste Bild, da es immer das erste Bild des Videos ist
    und in der Regel kein relevantes Bild darstellt (z.B. schwarzer Bildschirm, Intro).
    """
    print(f"Entferne erstes Bild {final_images_to_save[0][0].name} aus der Liste, da es das erste Video-Bild ist.")
    final_images_to_save.pop(0) 

    print(f"\nSpeichere {len(final_images_to_save)} finale Bilder...")
    for filename, image in final_images_to_save:
        image.save(filename, format=pillow_fmt, quality=95)
        print(f"-> {filename} gespeichert.")

    print("Fertig – alle relevanten Frames wurden gespeichert.")
