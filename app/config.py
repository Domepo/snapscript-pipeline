import os

# Name der Datenbankdatei
DB_NAME = "presentation_slides.db"

# Ollama Modellname
OLLAMA_MODEL = 'gemma3:27b' # oder 'llava', 'gemma:2b' etc.

OLLAMA_NUM_CTX = 50

YOLO_MODELL = 'data/weights/best.pt'

TRANSCRIPT_PATH = "data/transcript/transcript.txt"

TPYST_INPUT_PATH = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data/typst/lecture.typ"
TYPST_PDF_OUTPUT_PATH   = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data/typst/lecture.pdf"
ROOT_DIRECTORY    = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data"

# Lade Transkripttext aus Datei (falls vorhanden)
try:
    with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
        FULL_TRANSCRIPT_TEXT = f.read()
except FileNotFoundError:
    print(f"WARNUNG: Transkriptdatei '{TRANSCRIPT_PATH}' nicht gefunden.")
