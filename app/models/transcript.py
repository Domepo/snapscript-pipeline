from .database import get_connection
import logging
def add_transcript(full_text: str) -> int | None:
    """Fügt ein neues Transkript hinzu und gibt dessen ID zurück."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO transcripts (full_text) VALUES (?)", (full_text,))
        transcript_id = cursor.lastrowid
        conn.commit()
        logging.info(f"Transkript erfolgreich hinzugefügt mit ID: {transcript_id}")
        return transcript_id
    except Exception as e:
        logging.info(f"Fehler beim Hinzufügen des Transkripts: {e}")
        return None
    finally:
        conn.close()

def get_transcript_by_id(transcript_id: int) -> str | None:
    """Holt den Volltext eines Transkripts anhand seiner ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT full_text FROM transcripts WHERE id = ?", (transcript_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None