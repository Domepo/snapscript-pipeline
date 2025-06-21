from .database import get_connection
import logging

def add_image_marker(transcript_id: int, image_path: str, char_offset: int, matched_text_snippet: str = ""):
    """Fügt einen Bildmarker für ein Transkript hinzu."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO image_markers (transcript_id, image_path, char_offset, matched_text_snippet)
            VALUES (?, ?, ?, ?)
        ''', (transcript_id, image_path, char_offset, matched_text_snippet))
        conn.commit()
        logging.info(f"Bildmarker für '{image_path}' bei Offset {char_offset} (Transkript ID: {transcript_id}) hinzugefügt.")
    except Exception as e:
        logging.info(f"Fehler beim Hinzufügen des Bildmarkers: {e}")
    finally:
        conn.close()

def get_image_markers_for_transcript(transcript_id: int) -> list:
    """Holt alle Bildmarker für ein Transkript, sortiert nach char_offset."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT image_path, char_offset, matched_text_snippet
        FROM image_markers
        WHERE transcript_id = ?
        ORDER BY char_offset ASC
    ''', (transcript_id,))
    markers = [{"image_path": row[0], "char_offset": row[1], "matched_text_snippet": row[2]} for row in cursor.fetchall()]
    conn.close()
    return markers