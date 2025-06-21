from ultralytics import YOLO
from services.ollama_fix_yolo_service import yolo_fix
from utils.validate_crop_image import is_empty_or_two_tone
import os
import config
import cv2
import time
import logging
def box_inside(box_a, box_b):
    """Prüft, ob box_a komplett innerhalb von box_b liegt."""
    xa1, ya1, xa2, ya2 = box_a
    xb1, yb1, xb2, yb2 = box_b
    return xa1 >= xb1 and ya1 >= yb1 and xa2 <= xb2 and ya2 <= yb2

def get_crop_image(image_folder:str = "data/tmp",  output_folder:str = "data/cropped", cropped_fail_folder:str = "data/cropped_failed") -> None: 
    # Modell laden
    model = YOLO(config.YOLO_MODELL)

    os.makedirs(output_folder, exist_ok=True)
    saved_crops = []  

    os.makedirs(cropped_fail_folder, exist_ok=True)

    for file in os.listdir(image_folder):

        base, ext = os.path.splitext(file)  
        file_number = int(base) 

        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img_path = os.path.join(image_folder, file)
        img = cv2.imread(img_path)

        results = model(img_path)[0]

        if len(results.boxes) == 0:
            logging.info(f"Keine Objekte in {file}")
            continue

        # Nur Klasse 0
        boxes = results.boxes
        xyxy = boxes.xyxy.cpu().numpy()
        cls = boxes.cls.cpu().numpy()

        class0_boxes = [xyxy[i] for i, c in enumerate(cls) if int(c) == 0]

        if not class0_boxes:
            logging.info(f"Keine Klasse-0-Boxen in {file}")
            continue

        # Innere Boxen entfernen
        filtered_boxes = []
        for i, box_a in enumerate(class0_boxes):
            keep = True
            for j, box_b in enumerate(class0_boxes):
                if i != j and box_inside(box_a, box_b):
                    keep = False
                    break
            if keep:
                filtered_boxes.append(box_a)

        # Schritt 1: Alle Bilder croppen und speichern
        for idx, box in enumerate(filtered_boxes):
            x1, y1, x2, y2 = map(int, box)
            crop = img[y1:y2, x1:x2]

            out_path = os.path.join(output_folder, f"{file_number+idx}{ext}")
            cv2.imwrite(out_path, crop)
            logging.info(f"Gespeichert: {out_path}")

            saved_crops.append((out_path, f"FAILED_crop_{file_number+idx}{ext}"))

    # Schritt 2: Prüfen & ggf. verschieben
    for original_path, failed_filename in saved_crops:
        validate_image = is_empty_or_two_tone(original_path,
                            var_thresh=5.0,
                            lap_var_thresh=50.0,
                            unique_gray_thresh=3)
        
        if not yolo_fix(original_path) or validate_image:
            failed_path = os.path.join(cropped_fail_folder, failed_filename)
            os.rename(original_path, failed_path)
            logging.info(f"❌ Verschoben nach: {failed_path}")
