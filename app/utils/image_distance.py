from PIL import Image
import imagehash
import os
import itertools
import matplotlib.pyplot as plt
def compare_successive_images_folder(image_folder:str):

    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Hashes berechnen
    hashes = {}
    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        img = Image.open(img_path)
        hashes[img_file] = imagehash.phash(img)

    # Paare vergleichen
    differences = []
    for i in range(len(image_files) - 1):
        file1 = image_files[i]
        file2 = image_files[i + 1]
        hash1 = hashes[file1]
        hash2 = hashes[file2]
        
        diff = hash1 - hash2

        if(diff > 20):
            differences.append((diff, file1, file2))

    # Sortieren: größte Unterschiede zuerst
    differences.sort(reverse=True)


    for diff, file1, file2 in differences:
        # Neuen Namen definieren
        # Beispiel: "_DIFFERENT" anhängen vor Dateiendung
        name, ext = os.path.splitext(file2)
        new_name = f"{name}_DIFFERENT{ext}"
        
        # Pfade bauen
        old_path = os.path.join(image_folder, file2)
        new_path = os.path.join(image_folder, new_name)
        
        # Umbenennen
        os.rename(old_path, new_path)
        
        print(f"{file1} <-> {file2} | Unterschied: {diff}")

def compare_successive_images(image1:Image.Image, image2:Image.Image):
    """
    Vergleicht zwei Bilder und gibt den Unterschied in der Hash-Distanz zurück.
    """

    # image1 = Image.open(image1)
    # image2 = Image.open(image2)

    hash1 = imagehash.phash(image1)
    hash2 = imagehash.phash(image2)

    diff = hash1 - hash2
    
    return diff
# print(compare_successive_images("data/tmp/test/0000059200.jpg","data/tmp/test/0000438800.jpg"))