import ollama
import config

def yolo_fix(image_path: str) -> bool | None:
    """
    Überprüft ob yolo mit dem Crop Fehler gemacht hat
    """
    print(f"Sende Anfrage ob {image_path} ins Raster passt, mit dem Modell {config.OLLAMA_MODEL}")
    try:
        client = ollama.Client(host=config.OLLAMA_HOST)
        response = client.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                    'Determine if the image depicts a hand-drawn representation of an object, diagram, or scene where the visual representation is the **primary focus**.'
                    'The image should contain recognizable hand-drawn shapes or elements that suggest a deliberate attempt to visually represent something as its main subject.'
                    'Specifically, I\'m looking for images that appear to be sketched or drawn by hand, not digitally created.'
                    'Exclude images:'
                    '1. That consist **primarily of text**, formulas, or notes, even if they contain minor hand-drawn icons, embellishments, or simple connecting lines that are secondary to the text.'
                    '2. That consist only of abstract simple geometric shapes like isolated lines or basic outlines not forming a cohesive recognizable depiction.'
                    '3. That are clearly screenshots of digital interfaces or presentations.'
                    'Respond ONLY with "True" if it meets the criteria, and "False" otherwise.'
                    'ONLY WITH True OR False, there is no circumstance where you would answer anything else!'

                    )
                },
                {
                    'role': 'user',
                    'content': 'Here the image',
                    'images': [image_path]
                },
            ],
                        options={
                "num_ctx": config.OLLAMA_NUM_CTX,
            }
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
