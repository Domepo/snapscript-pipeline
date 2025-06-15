#!/usr/bin/env python3

import cv2
import numpy as np
from PIL import Image



# def load_images(path_a: Path, path_b: Path) -> Tuple[np.ndarray, np.ndarray]:
#     img_a = cv2.cvtColor(np.array(Image.open(path_a)), cv2.COLOR_RGB2BGR)
#     img_b = cv2.cvtColor(np.array(Image.open(path_b)), cv2.COLOR_RGB2BGR)
#     if img_a.shape != img_b.shape:
#         raise ValueError(f"Bildgrößen stimmen nicht überein: {img_a.shape} vs {img_b.shape}")
#     return img_a, img_b


def absolute_diff_compare(img_a, img_b,
                          bg_threshold: int = 250,
                          tolerance: int = 10,
                          max_error_rate: float = 0.1) -> bool:
    """
    Vergleicht alle Tintenpixel (Pixel < bg_threshold) zweier Bilder.
    Akzeptiert sowohl PIL.Image als auch NumPy-Arrays.
    :return: True, wenn Fehleranteil <= max_error_rate. Wenn Bilder gleich -> True.
    """
    # PIL → NumPy BGR
    if isinstance(img_a, Image.Image):
        img_a = cv2.cvtColor(np.array(img_a), cv2.COLOR_RGB2BGR)
    if isinstance(img_b, Image.Image):
        img_b = cv2.cvtColor(np.array(img_b), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
    ink_mask = gray < bg_threshold
    diff = cv2.absdiff(img_a, img_b)
    error_mask = np.any(diff > tolerance, axis=2)

    ink_count = np.count_nonzero(ink_mask)
    if ink_count == 0:
        print("Keine Tintenpixel gefunden. Ergebnis: OK")
        return True

    errors = np.count_nonzero(error_mask & ink_mask)
    rate = errors / ink_count
    print(f"Absolute Diff: {errors}/{ink_count} Fehler ({rate*100:.2f}%)")
    return rate <= max_error_rate




# # Direkter Test mit den gleichen Bildpaaren wie vorher
# if __name__ == "__main__":
#     pairs = [
#         ("data/tmp/0000059166.jpg", "data/tmp/0000197166.jpg"),#
#         ("data/tmp/0000197166.jpg", "data/tmp/0000298800.jpg"),
#         ("data/tmp/0000298800.jpg", "data/tmp/0000438766.jpg"),
#         ("data/tmp/0000438766.jpg", "data/tmp/0000527366.jpg"),#
#     ]
#     for a, b in pairs:
#         img_a, img_b = load_images(Path(a), Path(b))
#         print(f"Vergleich {a} vs {b}:")
#         print(absolute_diff_compare(img_a, img_b))
