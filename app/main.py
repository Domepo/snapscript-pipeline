import os
import config
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import images_in_transcript,compare_image_text_timestamp
from controllers.video_whisper import generate_transcript, store_transcript
from models.database import init_db
from utils.token_count import count_tokens
from utils.video_to_image_timestamp import extract_frames_rename_by_timestamp



if __name__ == "__main__":
    print("Starte den Prozess...")
    init_db()

    script = generate_transcript("data/videos/audiotest.mp3")
    transcript_id = store_transcript(script, config.TRANSCRIPT_PATH)

    # compare_image_text_timestamp("data/cropped/", transcript_id)
    """
    Change token count to run the model faster.
    """
    # config.OLLAMA_NUM_CTX = count_tokens(config.FULL_TRANSCRIPT_TEXT)



    # extract_frames_rename_by_timestamp("data/videos/Astro.mp4", "data/tmp")

    # get_crop_image("data/tmp", "data/cropped", "data/cropped_failed")

    # script_with_images = images_in_transcript("data/cropped", config.FULL_TRANSCRIPT_TEXT)






    # script = transcript_to_script(script_with_images)
    # config.OLLAMA_NUM_CTX = count_tokens(script)

    # print(script)
    # keywords = create_keywords(script)
    # print(keywords)
    # create_typst_document(script, keywords)