#!/usr/bin/env python3
"""
pixel_compare.py

Vergleicht nicht-weiße Pixel zweier Bilder (PIL) auf Toleranz
und ermöglicht automatische Toleranzbestimmung.
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image


def all_pixels_of_A_in_B(image1_pil: Image.Image,
                         image2_pil: Image.Image,
                         bg_threshold: int = 250,
                         tolerance: int | None = None,
                         auto_percentile: float = 99.0) -> bool:
    """
    Vergleicht alle nicht-weißen Pixel in image1_pil mit den entsprechenden
    Pixeln in image2_pil.

    :param image1_pil: PIL-Image mit Inhalt („Tinte"). / Vergleichsbild
    :param image2_pil: PIL-Image als Referenz. /  Orignal Bild 
    :param bg_threshold: Grauwert (0–255) ab dem ein Pixel als weiß gilt.
    :param tolerance: maximale Differenz pro Farbkanal (0–255).
                       Wenn None, wird automatisch basierend auf dem
                       `auto_percentile`-Quantil der Differenz gewählt.
    :param auto_percentile: Perzentil (0–100) für automatische Toleranz.
    :return: True, wenn alle Tinten-Pixel innerhalb der Toleranz liegen.
    """
    # Konvertierung PIL(RGB) → NumPy(BGR)
    img_a = cv2.cvtColor(np.array(image1_pil), cv2.COLOR_RGB2BGR)
    img_b = cv2.cvtColor(np.array(image2_pil), cv2.COLOR_RGB2BGR)

    # Größenprüfung
    if img_a.shape != img_b.shape:
        raise ValueError(f"Bildgrößen stimmen nicht überein: {img_a.shape} vs {img_b.shape}")

    # Maske aller Pixel < bg_threshold (Tinten-Pixel)
    gray_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    ink_mask = gray_a < bg_threshold

    # Absolute Differenz nur im Tintenbereich
    diff = cv2.absdiff(img_a, img_b)       # H x W x 3
    diff_ink = diff[ink_mask]             # N x 3

    # Wenn keine Tinten-Pixel → True
    if diff_ink.size == 0:
        return True

    # Automatische Toleranzbestimmung
    if tolerance is None:
        flat = diff_ink.flatten()
        tolerance = int(np.percentile(flat, auto_percentile))
        # print(f"Automatisch gewählte Toleranz ({auto_percentile}%-Quantil): {tolerance}")

    # Prüfen, ob ein Kanal die Toleranz überschreitet
    return np.any(diff_ink > tolerance)


def test_every(dir_a: str,
               dir_b: str,
               bg_threshold: int = 250,
               tolerance: int | None = None,
               auto_percentile: float = 99.0):
    """
    Testet alle Kombinationen von Bildern aus zwei Verzeichnissen.

    :param dir_a: Pfad zum Ordner mit zu vergleichenden Bildern.
    :param dir_b: Pfad zum Ordner mit Referenzbildern.
    :param bg_threshold: Grauwert für weißen Hintergrund.
    :param tolerance: maximale Kanal-Differenz oder None für automatische.
    :param auto_percentile: Perzentil der Differenz für automatische Toleranz.
    """
    dir_a = Path(dir_a)
    dir_b = Path(dir_b)
    files_a = sorted(dir_a.glob("*.[pj][pn]g"))
    files_b = sorted(dir_b.glob("*.[pj][pn]g"))

    for file_a in files_a:
        for file_b in files_b:
            img_a = Image.open(file_a)
            img_b = Image.open(file_b)
            ok = all_pixels_of_A_in_B(img_a, img_b,
                                     bg_threshold=bg_threshold,
                                     tolerance=tolerance,
                                     auto_percentile=auto_percentile)
            if(ok == False):
                print(f"{file_a.name:25s} vs {file_b.name:25s} -> ok? {ok}")


if __name__ == "__main__":
    # Beispiel-Aufruf: Alle Bilder in data/tmp/A vs alle in data/tmp/B
    # test_every("data/tmp", "data/tmp", bg_threshold=250, tolerance=None, auto_percentile=99.0)
    img_a = Image.open("data/tmp/0000377766.jpg")
    img_b = Image.open("data/tmp/0000377766.jpg")

    img_b = Image.open("data/tmp/0000427233.jpg")
    print(all_pixels_of_A_in_B(img_a,img_b))
