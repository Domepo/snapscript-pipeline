
#https://stackoverflow.com/questions/78389839/check-if-the-given-image-is-a-crop-of-another-bigger-image
from PIL import Image
import numpy as np
import cv2
import logging

def check_if_image_contains_image(image1_pil, image2_pil) -> bool:
    """
    image1 = cropped image
    image2 = original image
    """
    image1_cv = cv2.cvtColor(np.array(image1_pil), cv2.COLOR_RGB2BGR)
    image2_cv = cv2.cvtColor(np.array(image2_pil), cv2.COLOR_RGB2BGR)

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(image1_cv, None)
    kp2, des2 = sift.detectAndCompute(image2_cv, None)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

    return len(good_matches) > 50

# p2 = "data\lecture_images\Astro-3.jpg"
# p1 = "data\cropped\crop_0_Astro-3.jpg"

# image1_pil = Image.open(p1).convert("RGB")
# image2_pil = Image.open(p1).convert("RGB")

# # an die Funktion übergeben
# result = check_if_image_contains_image(image1_pil, image2_pil)
# print(result)


# def check_if_image_contains_image1(image1_path: str, image2_path: str) -> bool:
#     image1 = cv2.imread(image1_path)
#     image2 = cv2.imread(image2_path)

#     sift = cv2.SIFT_create()
#     kp1, des1 = sift.detectAndCompute(image1, None)
#     kp2, des2 = sift.detectAndCompute(image2, None)
#     bf = cv2.BFMatcher()
#     matches = bf.knnMatch(des1, des2, k=2)
#     good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

#     if len(good_matches) > 50:
#         return True
#     else:
#         return False
# print(check_if_image_contains_image1(p1,p2))