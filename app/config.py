import os
import logging
# Name der Datenbankdatei
DB_NAME = "presentation_slides.db"

# Ollama Modellname
OLLAMA_MODEL = 'gemma3:27b' # oder 'llava', 'gemma:2b' etc.
OLLAMA_HOST = "http://ollama:11434"


OLLAMA_NUM_CTX = 4096

YOLO_MODELL = 'data/weights/best.pt'

TRANSCRIPT_PATH = "data/transcript/transcript.txt"

TPYST_INPUT_PATH = "data/typst/lecture.typ"
ROOT_DIRECTORY    = "data"

# Lade Transkripttext aus Datei (falls vorhanden)
try:
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        FULL_TRANSCRIPT_TEXT = f.read()
except FileNotFoundError:
    logging.info(f"WARNUNG: Transkriptdatei '{TRANSCRIPT_PATH}' nicht gefunden.")
