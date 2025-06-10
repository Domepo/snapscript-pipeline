from services.ollama_fix_lecture_service import lecture_fix
import whisper
from whisper.utils import get_writer
import config
import re

def video_transcript(video_path:str, output_path:str = config.TRANSCRIPT_PATH) -> None:
    """
    Convert Video to Transcript txt
    """
    model = whisper.load_model("turbo")

    # Video transkribieren
    result = model.transcribe(video_path)

    srt_writer = get_writer("srt", "data/videos")
    srt_writer(result, "text.srt")

    raw_text = result["text"]

    # Satzzeichen erkennen (aber keine "...")
    formatted_text = re.sub(r'(?<!\.)\.{1}(?!\.)\s+', '.\n', raw_text)  # Punkt
    formatted_text = re.sub(r'(?<!!)[!]\s+', '!\n', formatted_text)     # Ausrufezeichen
    formatted_text = re.sub(r'(?<!\?)[?]\s+', '?\n', formatted_text)    # Fragezeichen

    # "..." entfernen oder belassen
    cleaned_text = formatted_text.replace("...", "")  # oder lassen, wenn gewünscht

    # Speichern
    # fixed_text = lecture_fix(cleaned_text)
    output_path = output_path
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Transkript mit Absätzen gespeichert unter: {output_path}")

