import os
import config
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import images_in_transcript
from lecture.video_whisper import video_transcript
from lecture.pdf_extractor import convert_pdfs_in_folder
from utils.token_count import count_tokens



if __name__ == "__main__":
    print("Starte den Prozess...")

    #video_transcript("data/videos/Astro.mp4",config.TRANSCRIPT_PATH)
    """
    Change token count to run the model faster.
    """
    config.OLLAMA_NUM_CTX = count_tokens(config.FULL_TRANSCRIPT_TEXT)

    # convert_pdfs_in_folder("data/pdf", "data/lecture_images")
    # get_crop_image("data/lecture_images", "data/cropped", "data/cropped_failed")

    script_with_images = images_in_transcript("data/cropped", config.FULL_TRANSCRIPT_TEXT)

    script = transcript_to_script(script_with_images)
    config.OLLAMA_NUM_CTX = count_tokens(script)

    print(script)
    keywords = create_keywords(script)
    print(keywords)
    create_typst_document(script, keywords)