import os
import config
import json
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script_iterative
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import compare_image_text_timestamp
from controllers.video_whisper import generate_transcript, store_transcript
from models.database import init_db
from utils.token_count import count_tokens
from utils.video_to_image_timestamp import extract_frames_rename_by_timestamp


if __name__ == "__main__":
    print("Starte den Prozess...")
    init_db()
    
    video_path = "data/videos/Astro.mp4"
    script = generate_transcript(video_path)

    transcript_id = store_transcript(script, config.TRANSCRIPT_PATH)

    extract_frames_rename_by_timestamp(video_path, "data/tmp")

    """
    Change token count to run the model faster.
    """
    config.OLLAMA_NUM_CTX = count_tokens(config.FULL_TRANSCRIPT_TEXT)


    get_crop_image("data/tmp", "data/cropped", "data/cropped_failed")
    
    script_with_images = compare_image_text_timestamp("data/cropped", transcript_id ,"data/transcript/transcript_with_images.txt")
    
    config.OLLAMA_NUM_CTX = count_tokens(script_with_images)


    print(script_with_images)

    final_script = transcript_to_script_iterative(script_with_images)


    print(script_with_images)

    keywords = create_keywords(final_script)
    print(keywords)
    create_typst_document(final_script, keywords)