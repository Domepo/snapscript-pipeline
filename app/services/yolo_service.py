from ultralytics import YOLO
from services.ollama_fix_yolo_service import yolo_fix
import os
import cv2

def box_inside(box_a, box_b):
    """Prüft, ob box_a komplett innerhalb von box_b liegt."""
    xa1, ya1, xa2, ya2 = box_a
    xb1, yb1, xb2, yb2 = box_b
    return xa1 >= xb1 and ya1 >= yb1 and xa2 <= xb2 and ya2 <= yb2

def get_crop_image(): 
    # Modell laden
    model = YOLO("data/weights/best.pt")

    # Neue Pfade
    image_folder = "data/images"
    output_folder = "data/cropped"
    os.makedirs(output_folder, exist_ok=True)

    # Bilder durchgehen
    saved_crops = []  # (original_path, failed_path_candidate)

    for file in os.listdir(image_folder):
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        img_path = os.path.join(image_folder, file)
        img = cv2.imread(img_path)

        results = model(img_path)[0]

        if len(results.boxes) == 0:
            print(f"Keine Objekte in {file}")
            continue

        # Nur Klasse 0
        boxes = results.boxes
        xyxy = boxes.xyxy.cpu().numpy()
        cls = boxes.cls.cpu().numpy()

        class0_boxes = [xyxy[i] for i, c in enumerate(cls) if int(c) == 0]

        if not class0_boxes:
            print(f"Keine Klasse-0-Boxen in {file}")
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

        # Croppen & Speichern
        # for idx, box in enumerate(filtered_boxes):
        #     x1, y1, x2, y2 = map(int, box)
        #     crop = img[y1:y2, x1:x2]
        #     out_path = os.path.join(output_folder, f"crop_{idx}_{file}")
        #     cv2.imwrite(out_path, crop)
        #     print(f"Gespeichert: {out_path}")

            # if not yolo_fix(out_path):
            #     failed_path = os.path.join(output_folder, f"FAILED_crop_{idx}_{file}")
            #     os.rename(out_path, failed_path)
            #     print(f"❌ Umbenannt in: {failed_path}")


        # Schritt 1: Alle Bilder croppen und speichern
        for idx, box in enumerate(filtered_boxes):
            x1, y1, x2, y2 = map(int, box)
            crop = img[y1:y2, x1:x2]
            out_path = os.path.join(output_folder, f"crop_{idx}_{file}")
            cv2.imwrite(out_path, crop)
            print(f"Gespeichert: {out_path}")
            
            # Für spätere Prüfung merken
            saved_crops.append((out_path, f"FAILED_crop_{idx}_{file}"))

        # Schritt 2: Nachträglich prüfen und ggf. umbenennen
    for original_path, failed_filename in saved_crops:
        if not yolo_fix(original_path):
            failed_path = os.path.join(output_folder, failed_filename)
            os.rename(original_path, failed_path)
            print(f"❌ Umbenannt in: {failed_path}")
