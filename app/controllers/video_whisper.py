import sqlite3
import whisper
from whisper.utils import get_writer
import config
import re
from services.ollama_fix_lecture_service import lecture_fix
from utils.measure_time import measure_time
from models.database import init_db
from models.database import get_connection

def timestamp_to_milliseconds(ts: str) -> int:
    """Konvertiert Timestamp 'HH:MM:SS,mmm' in Millisekunden."""
    h, m, s_ms = ts.split(":")
    s, ms = s_ms.split(",")
    total_ms = (
        int(h) * 3600 * 1000 +
        int(m) * 60 * 1000 +
        int(s) * 1000 +
        int(ms)
    )
    return total_ms
@measure_time
def generate_transcript(video_path:str) -> dict:
    """
    Transkribiert Video und schreibt SRT. Gibt Transkript-Resultat zurück.
    """
    model = whisper.load_model("turbo")

    # Video transkribieren
    result = model.transcribe(video_path)

    # SRT schreiben
    srt_writer = get_writer("srt", "data/videos")
    srt_writer(result, "text.srt")

    print(f"SRT gespeichert: data/videos/text.srt")
    return result
@measure_time
def store_transcript(result: dict, output_path:str = config.TRANSCRIPT_PATH) -> None:
    """
    Speichert Transkript (full_text + Zeilen) in DB und schreibt cleaned text in Datei.
    """
    raw_text = result["text"]

    # Satzzeichen erkennen
    formatted_text = re.sub(r'(?<!\.)\.{1}(?!\.)\s+', '.\n', raw_text)  # Punkt
    formatted_text = re.sub(r'(?<!!)[!]\s+', '!\n', formatted_text)     # Ausrufezeichen
    formatted_text = re.sub(r'(?<!\?)[?]\s+', '?\n', formatted_text)    # Fragezeichen

    # "..." entfernen
    cleaned_text = formatted_text.replace("...", "")

    # --- Save Full Text in DB ---
    conn = get_connection()
    cursor = conn.cursor()

    # Insert full_text into transcripts table
    cursor.execute('''
        INSERT INTO transcripts (full_text)
        VALUES (?)
    ''', (cleaned_text,))
    transcript_id = cursor.lastrowid

    # --- Parse SRT and insert lines ---
    srt_path = "data/videos/text.srt"
    with open(srt_path, "r", encoding="utf-8") as srt_file:
        srt_content = srt_file.read()

    # SRT block parser (Timestamp + Text)
    srt_blocks = re.split(r'\n\s*\n', srt_content.strip())

    for block in srt_blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 2:
            timestamp_line = lines[0] if "-->" in lines[0] else lines[1]
            match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})', timestamp_line)
            if match:
                start_timestamp = match.group(1)
                end_timestamp = match.group(2)

                start_ms = timestamp_to_milliseconds(start_timestamp)
                end_ms = timestamp_to_milliseconds(end_timestamp)

                # Zeilentext zusammenbauen
                line_text = ' '.join(lines[1:]) if "-->" in lines[0] else ' '.join(lines[2:])

                # Insert in DB
                cursor.execute('''
                    INSERT INTO transcript_lines (transcript_id, start_timestamp, end_timestamp, line_text)
                    VALUES (?, ?, ?, ?)
                ''', (transcript_id, start_ms, end_ms, line_text.strip()))

    # Finalize
    conn.commit()
    conn.close()

    # Save cleaned text also to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    print(f"Transkript gespeichert unter: {output_path}")
    print(f"Transkript + Zeilen in DB gespeichert (transcript_id={transcript_id})")
    return transcript_id

