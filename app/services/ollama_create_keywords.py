import ollama
import config
from utils.measure_time import measure_time
import logging
@measure_time
def create_keywords(full_transcript_text: str) -> str | None:
    """
    Erstellt 5-10 Keywords aus dem Transkripttext.
    """
    logging.info(f"Sende Anfrage an Ollama mit Modell {config.OLLAMA_MODEL}")
    try:
        client = ollama.Client(host=config.OLLAMA_HOST)
        response = client.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'Fasse den Text in 5-10 Keywords zusammen.' 
                        'Jedes Keyword sollte nur ein einzelnes Wort sein.' 
                        'Gib die Keywords in folgendem Format aus: """["Keyword1", "Keyword2"]"""'
                        'DU DARFST NUR DIE KEYWORDS AUSGEBEN UND KEINE ERKLÄRUNG DAZU GEBEN.'
                        'KEINE ANDEREN SACHEN AUSGEBEN, NUR DIE KEYWORDS!'

                    )
                },
                {
                    'role': 'user',
                    'content': f"Hier ist der vollständige Transkripttext:\n\n{full_transcript_text}"
                }
            ],            
            options={
                "num_ctx": config.OLLAMA_NUM_CTX,
            }
        )
        if response and 'message' in response and 'content' in response['message']:
            fixed_transrcibt = response['message']['content'].strip()
            if fixed_transrcibt:
                return fixed_transrcibt 
            else:
                logging.info("Ollama hat einen leeren Abschnitt zurückgegeben.")
                return None
        else:
            logging.info("Unerwartete Antwortstruktur von Ollama:", response)
            return None

    except Exception as e:
        logging.info(f"Ein Fehler bei der Kommunikation mit Ollama ist aufgetreten: {e}")
        return None