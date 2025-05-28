import ollama
import config

def yolo_fix(image_path: str) -> bool | None:
    """
    Überprüft ob yolo mit dem Crop Fehler gemacht hat
    """
    print(f"Sende Anfrage ob {image_path} ins Raster passt, mit dem Modell {config.OLLAMA_MODEL}")
    try:
        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'Determine if the image depicts a hand-drawn representation of an object, diagram, or scene.' 
                        'The image should contain recognizable shapes or elements that suggest a deliberate attempt to visually represent something.'
                        ' Specifically, Im looking for images that appear to be sketched or drawn by hand, not digitally created. Exclude images that consist solely of'
                        ' text, formulas, or simple geometric shapes like lines or basic outlines, or that are clearly screenshots of digital interfaces or presentations.'
                        'Respond ONLY with "True" if it meets the criteria, and "False" otherwise. ONLY WITH True OR False, there is no circumstance where you would answer anything else!'


                    )
                },
                {
                    'role': 'user',
                    'content': 'Here the image',
                    'images': [image_path]
                },
            ]
        )
        if response and 'message' in response and 'content' in response['message']:
            fixed_transrcibt = response['message']['content'].strip()
            if fixed_transrcibt == "True":
                return True 
            elif fixed_transrcibt == "False":
                return False 
            else:
                print("Ollama hat einen leeren Abschnitt zurückgegeben.")
                return None
        else:
            print("Unerwartete Antwortstruktur von Ollama:", response)
            return None

    except Exception as e:
        print(f"Ein Fehler bei der Kommunikation mit Ollama ist aufgetreten: {e}")
        return None
