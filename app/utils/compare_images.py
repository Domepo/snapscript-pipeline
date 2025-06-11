import cv2
import numpy as np
from pathlib import Path
from PIL import Image
def all_pixels_of_A_in_B(image1_pil,
                         image2_pil,
                         bg_threshold: int = 250,
                         tolerance: int = 30) -> bool:
    """
    image1_pil ⇢ Pfad zum Vergleichsbild

    image2_pil ⇢ Pfad zum Orignalen Bild 

    True ⇢ alle nicht-weißen Pixel von Bild A stimmen (innerhalb 'tolerance')
           mit den entsprechenden Pixeln in Bild B überein.
    False ⇢ mindestens ein solcher Pixel weicht zu stark ab.
    
    • bg_threshold … Grauwert, ab dem ein Pixel als „weiß / leer“ gilt (0–255)
    • tolerance    … maximal zulässige Differenz pro Farbkanal (0–255)
    """
    img_a = cv2.cvtColor(np.array(image1_pil), cv2.COLOR_RGB2BGR)
    img_b = cv2.cvtColor(np.array(image2_pil), cv2.COLOR_RGB2BGR)

    # img_a = cv2.imread(path_a, cv2.IMREAD_COLOR)
    # img_b = cv2.imread(path_b, cv2.IMREAD_COLOR)

    if img_a is None or img_b is None:
        raise FileNotFoundError("Mindestens eines der Bilder konnte nicht geladen werden.")

    # beide Bilder müssen gleich groß sein – sonst vorher zuschneiden / resizen
    if img_a.shape != img_b.shape:
        raise ValueError("Die Bildgrößen stimmen nicht überein.")

    # 1) Maske für alle Nicht-Hintergrund-Pixel in A
    gray_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    content_mask = gray_a < bg_threshold          # True = „Tinte“, False = „weiß“

    # 2) Pixel-Differenz nur an diesen Stellen ansehen
    diff = cv2.absdiff(img_a, img_b)
    diff_masked = diff[content_mask]

    # 3) Prüfen, ob irgendwo ein Kanal die Toleranz überschreitet
    if diff_masked.size == 0:
        return False  # A enthält gar keine „Tinte“

    max_diff = diff_masked.max()
    return max_diff <= tolerance

print(all_pixels_of_A_in_B(
    image1_pil=Image.open("data/tmp/0000059200.jpg").convert("RGB"),
    image2_pil=Image.open("data/tmp/0000197200.jpg").convert("RGB")
))