import os
import config
from models.database import init_db
from models.transcript import add_transcript
from models.image_marker import add_image_marker
from services.ollama_service import get_relevant_section
from services.yolo_service import get_crop_image
from controllers.transcript_controller import images_in_transcript
from utils.text_utils import find_section_end_offset 
from lecture.video_whisper import video_transcript
from lecture.pdf_extractor import convert_pdfs_in_folder



if __name__ == "__main__":
    # video_transcript("data/videos/Download.mp4")
    # convert_pdfs_in_folder("data/pdf", "data/lecture_images")
    # get_crop_image("data/lecture_images", "data/cropped", "data/cropped_failed")
    images_in_transcript("data/cropped")
    # main()

