import ollama
import config
from services.fuzzing_service import find_paragraph_with_fuzzing

def get_relevant_section(image_path: str, full_transcript_text: str) -> str | None:
    """
    Sendet das Bild und den VOLLSTÄNDIGEN Transkripttext an Ollama und gibt den relevanten Abschnitt zurück.
    Gibt None zurück, wenn ein Fehler auftritt oder keine Antwort erhalten wird.
    """
    print(f"Sende Anfrage an Ollama mit Modell {config.OLLAMA_MODEL} für Bild {image_path}...")
    try:
        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'Du bekommst ein Bild einer Folie aus einem Video und den transkribierten Text desselben Videos. '
                        'Deine Aufgabe ist es, den Abschnitt im Transkript zu finden, der am besten zur Folie passt. '
                        'Gib mir nur diesen passenden Abschnitt aus dem Transkript wieder, ohne zusätzliche Erklärungen, Einleitungen oder Formatierungen wie Markdown.'
                        'Folgende Schritte sollst du beachten:'
                        '1: Analysiere das Bild '
                        '2: Schaue dir genau an, welchen Text du auf dem Bild findest und übersetze ihn gegebenenfalls'
                        '3: Nimm diese Infos und vergleiche das mit dem gegebenen Text'
                        '4: Falls es übereinstimmungen gibt, gebe den ganzen Abschnitt aus, der sich darauf bezieht' 
                        'Beispiel: Wenn im Transkript steht "Das ist ein Test." und das Bild dazu passt, gib "Das ist ein Test." zurück, nicht "Ein Test" oder "Dies ist ein Test.." Also exat das gleiche was auch im Transkript steht. '
                    )
                },
                {
                    'role': 'user',
                    'content': 'Hier ist das Bild und der vollständige Transkripttext. Finde den exakt passenden Abschnitt im Transkript.',
                    'images': [image_path]
                },
                {
                    'role': 'user',
                    'content': f"Hier ist der vollständige Transkripttext:\n\n{full_transcript_text}"
                }
            ],            options={
                "num_ctx": config.OLLAMA_NUM_CTX + 1000, #höherer Kontext für Bilder
            }
        )
        if response and 'message' in response and 'content' in response['message']:
            relevant_section = response['message']['content'].strip()
            if relevant_section:
                # Zusätzliche Prüfung, ob der Abschnitt auch wirklich im Original vorkommt
                # Dies kann Ollama-Halluzinationen oder kleine Abweichungen abfangen
                relevant_section = find_paragraph_with_fuzzing(full_transcript_text,relevant_section)

                if relevant_section in full_transcript_text:
                    print(relevant_section)
                    return relevant_section
                else:
                    # Versuch einer "Fuzzy"-Suche oder Loggen des Problems
                    print(f"WARNUNG: Ollama-Abschnitt '{relevant_section[:50]}...' nicht exakt im Originaltext gefunden. Versuche Teilübereinstimmung.")
                    # Hier könnte man versuchen, den ähnlichsten Substring zu finden,
                    # aber das kann komplex werden. Fürs Erste geben wir None zurück oder den Teil, der passt.
                    # Eine einfache Prüfung:
                    # for i in range(len(full_transcript_text) - len(relevant_section) + 1):
                    #     if full_transcript_text[i:i+len(relevant_section)].strip() == relevant_section: # Vergleiche ohne Rand-Leerzeichen
                    #         return full_transcript_text[i:i+len(relevant_section)]
                    print("Exakter Abschnitt nicht gefunden, Ollama-Antwort könnte abweichen. Überprüfen Sie die Ollama-Antwort manuell.")
                    return None # Oder relevant_section, wenn man das Risiko eingehen will
            else:
                print("Ollama hat einen leeren Abschnitt zurückgegeben.")
                return None
        else:
            print("Unerwartete Antwortstruktur von Ollama:", response)
            return None

    except Exception as e:
        print(f"Ein Fehler bei der Kommunikation mit Ollama ist aufgetreten: {e}")
        return None