import numpy as np
import cv2


def is_empty_or_two_tone(img: np.ndarray,
                         var_thresh: float = 10.0,
                         lap_var_thresh: float = 20.0,
                         unique_gray_thresh: int = 3) -> bool:
    """
    True zurückgeben, wenn img entweder komplett gleichförmig, kantenarm
    oder nur two-tone (<= unique_gray_thresh Grauwert-Stufen) ist.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1) Grauwert-Varianz
    if np.std(gray) < var_thresh:
        return True

    # 2) Kanten-Varianz (Laplacian)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    if lap.var() < lap_var_thresh:
        return True

    # 3) Two-Tone-Check: zu wenige Graustufen?
    unique_vals = np.unique(gray)
    if len(unique_vals) <= unique_gray_thresh:
        # z.B. nur [0,255] oder [0,1,255]
        return True

    return False