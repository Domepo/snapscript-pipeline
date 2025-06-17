import ollama
import config

def lecture_fix(full_transcript_text: str) -> str | None:
    """
    Bearbeitet das von Whispier ausgebene Transkribt.
    """
    print(f"Sende Anfrage an Ollama mit Modell {config.OLLAMA_MODEL}")
    try:
        client = ollama.Client(host=config.OLLAMA_HOST)
        response = client.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'Du sollst das folgende Transkript inhaltlich nicht verändern, entferne nur unötige Satzzeichen, ähm oder ähnliches. Gehe wie folgt vor:'
                        '1. Erkenne um welches Thema es sich handelt'
                        '2. Schaue ob es Wörter gibt die Falsch Transkribiert wurden und passe Sie gegebenfalls an'
                        '3. Bilde vollständige Sätze, wenn diese frühzeitig unterbrochen wurden.'

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
                print("Ollama hat einen leeren Abschnitt zurückgegeben.")
                return None
        else:
            print("Unerwartete Antwortstruktur von Ollama:", response)
            return None

    except Exception as e:
        print(f"Ein Fehler bei der Kommunikation mit Ollama ist aufgetreten: {e}")
        return None