from pathlib import Path
from datetime import datetime, timedelta
from utils.image_distance import compare_successive_images
from utils.compare_images import all_pixels_of_A_in_B
import cv2
import numpy as np
from PIL import Image

def get_image_edges(img: Image.Image):
    """
    Berechnet die Kan
    """

    img_gray = np.array(img.convert("L"))
    edges = cv2.Canny(img_gray, 100, 200)
    num_edges = np.sum(edges > 0)

    return num_edges

def extract_frames_rename_by_timestamp(
    video_path: str,
    output_dir: str = "frames",
    image_format: str = "jpg",
    ts_pattern: str = "%Y%m%d_%H%M%S_%f",   # Dateinamen-Format
    recording_start: datetime | None = None # absoluter Startzeitpunkt
) -> None:
    """
    Liest ein Video frame-weise ein, speichert jedes Bild und benennt es nach
    seinem absoluten Timestamp (recording_start + Frame-Offset).

    Falls recording_start=None, wird der Zeitpunkt des Aufrufs verwendet.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Konnte Video '{video_path}' nicht öffnen.")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Falls kein expliziter Start übergeben wurde → jetzt
    if recording_start is None:
        recording_start = datetime.now().replace(microsecond=0)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    previous_img = None
    image_counter = 0

    for idx in range(total_frames):
        ok, frame_bgr = cap.read()
        if not ok:
            break


        elapsed_ms = int((idx / fps) * 1000)   # 6 700 ms → 0000006700
        ts_str = f"{elapsed_ms:010d}"
        file_name = out_path / f"{ts_str}.{image_format}"

        img = Image.fromarray(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))

        if previous_img is None:
            previous_img = img
            continue 
            
        """
        Berechnet den Unterschied zwischen zwei aufeinanderfolgenden Bildern mit hashing.
        Beispielaufruf:
        """
        image_difference = compare_successive_images(previous_img, img)
        

        if  image_difference > 25 and get_image_edges(previous_img) > 5000:
            print(f"Unterschied erkannt zwischen {previous_img} und {file_name} ist {image_difference}.")
            
            FORMAT_MAP = {
            "jpg":  "JPEG",
            "jpeg": "JPEG",
            "png":  "PNG",
            "tif":  "TIFF",
            }


            """
            Prüft ob ein Bild in dem anderen enthalten ist.
            Wenn ja, wird das Bild nicht gespeichert.
            """
            image_contains_same_iamge = all_pixels_of_A_in_B(previous_img,img)
            
            print(image_contains_same_iamge)
            if image_contains_same_iamge:
                print(f"Bild {file_name} ist ein Teil von {previous_img}. Überspringe Speicherung.")
                continue
            else:
                print("Das ist ein TEst")
            """
            Speichert nicht das erste Bild
            """
            print(image_counter)
            pillow_fmt = FORMAT_MAP[image_format.lower()]
            previous_img.save(file_name, format=pillow_fmt, quality=95)


        previous_img = img
        

    cap.release()
    print("Fertig – alle Frames wurden gespeichert.")



