import sqlite3
import config
import os

def get_connection():
    return sqlite3.connect(config.DB_NAME)

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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcript_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transcript_id INTEGER NOT NULL,
            start_timestamp TEXT NOT NULL,
            end_timestamp TEXT NOT NULL,
            line_text TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transcript_id) REFERENCES transcripts (id)
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Datenbank '{config.DB_NAME}' initialisiert und Tabellen 'transcripts' & 'image_markers' sichergestellt.")

def delete_db():
    """Löscht die SQLite-Datenbankdatei vollständig."""
    if os.path.exists(config.DB_NAME):
        os.remove(config.DB_NAME)
        print(f"Datenbank '{config.DB_NAME}' wurde gelöscht.")
    else:
        print(f"Datenbank '{config.DB_NAME}' existiert nicht.")