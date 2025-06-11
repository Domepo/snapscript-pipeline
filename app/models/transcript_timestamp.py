from .database import get_connection
def get_timestamps(transcript_id: int) -> list:
    """
    Holt alle Timestamps für ein Transkript.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT start_timestamp, end_timestamp
        FROM transcript_lines
        WHERE transcript_id = ?
    ''', (transcript_id,))
    timestamps = [{"start_timestamp": row[0], "end_timestamp": row[1]} for row in cursor.fetchall()]
    conn.close()
    return timestamps