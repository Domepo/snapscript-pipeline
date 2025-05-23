# database_operations.py

import sqlite3
import config

def init_db():
    """Initialisiert die Datenbank und erstellt die Tabellen, falls sie nicht existieren."""
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    # Tabelle für die vollständigen Transkripte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabelle für die Bildmarker innerhalb der Transkripte
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_markers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcript_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            char_offset INTEGER NOT NULL,
            matched_text_snippet TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transcript_id) REFERENCES transcripts (id)
        )
    ''')
    # Index für schnellere Abfragen der Marker pro Transkript
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_image_markers_transcript_id
        ON image_markers (transcript_id)
    ''')
    conn.commit()
    conn.close()
    print(f"Datenbank '{config.DB_NAME}' initialisiert und Tabellen 'transcripts' & 'image_markers' sichergestellt.")

def add_transcript(full_text: str) -> int | None:
    """Fügt ein neues Transkript hinzu und gibt dessen ID zurück."""
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO transcripts (full_text) VALUES (?)", (full_text,))
        transcript_id = cursor.lastrowid
        conn.commit()
        print(f"Transkript erfolgreich hinzugefügt mit ID: {transcript_id}")
        return transcript_id
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Transkripts: {e}")
        return None
    finally:
        conn.close()

def get_transcript_by_id(transcript_id: int) -> str | None:
    """Holt den Volltext eines Transkripts anhand seiner ID."""
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT full_text FROM transcripts WHERE id = ?", (transcript_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def add_image_marker(transcript_id: int, image_path: str, char_offset: int, matched_text_snippet: str = ""):
    """Fügt einen Bildmarker für ein Transkript hinzu."""
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO image_markers (transcript_id, image_path, char_offset, matched_text_snippet)
            VALUES (?, ?, ?, ?)
        ''', (transcript_id, image_path, char_offset, matched_text_snippet))
        conn.commit()
        print(f"Bildmarker für '{image_path}' bei Offset {char_offset} (Transkript ID: {transcript_id}) hinzugefügt.")
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Bildmarkers: {e}")
    finally:
        conn.close()

def get_image_markers_for_transcript(transcript_id: int) -> list:
    """Holt alle Bildmarker für ein Transkript, sortiert nach char_offset."""
    conn = sqlite3.connect(config.DB_NAME)
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