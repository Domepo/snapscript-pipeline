import os
from pdf2image import convert_from_bytes

def convert_pdfs_in_folder(pdf_folder: str, output_subfolder: str = "data/lecture_images") -> list:
    """
    Konvertiert alle PDF-Dateien in einem Ordner zu JPEG-Bildern.
    Gibt eine Liste der gespeicherten Bildpfade zurück.
    """
    output_folder = os.path.join(pdf_folder, output_subfolder)
    os.makedirs(output_folder, exist_ok=True)

    saved_images = []

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Konvertiere: {pdf_path}")

            with open(pdf_path, "rb") as f:
                images = convert_from_bytes(f.read())

            base_name = os.path.splitext(filename)[0]

            for i, image in enumerate(images):
                output_filename = f"{base_name}-{i+1}.jpg"
                image_path = os.path.join(output_folder, output_filename)
                image.save(image_path, "JPEG")
                saved_images.append(image_path)
                print(f"Gespeichert: {image_path}")

    return saved_images
