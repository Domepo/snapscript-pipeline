import ollama
import config

def transcript_to_script(full_transcript_text: str) -> str | None:
    """
    Schreib das Transcript in ein Skript für Vorlesungsinhalte um.
    """
    
    print(f"Sende Anfrage an Ollama mit Modell {config.OLLAMA_MODEL} ...")
    try:
        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (

f"""
"Du bist ein erfahrener Texter und Strukturierer von Transkripten. Deine Aufgabe ist es, ein langes Transkript in ein übersichtliches Format zu bringen, das eine kurze Zusammenfassung und detaillierte Abschnitte mit Überschriften enthält.
Anweisungen:
Zusammenfassung: Erstelle eine prägnante Zusammenfassung des Transkripts, die etwa 100 Wörter lang ist. Konzentriere dich auf die wichtigsten Punkte und Themen.
Überschriften: Identifiziere logische Abschnitte im Transkript und erstelle aussagekräftige Überschriften für jeden Abschnitt. Die Überschriften sollen den Inhalt des jeweiligen Abschnitts klar widerspiegeln.
Textbeibehaltung: Der ursprüngliche Text des Transkripts soll weitgehend unverändert bleiben. Nimm nur minimale Anpassungen vor, um die Lesbarkeit zu verbessern (z.B. Korrektur von Tippfehlern oder grammatikalischen Fehlern). Vermeide es, den Text zusammenzufassen oder zu kürzen. Schreibe die Abschnitte außerdem als Fließtext und vermeide Zeilenumbrüche innerhalb der Textblöcke.  Die Bilder im [] Format sollen an der Stelle bleiben, verändere diese nicht.
Formatierung: Formatiere das Ergebnis wie folgt:
# Titel

Hier die Zusammenfassung, mache es 100 Wörter lang

## Überschrift 1

Hier kommt der Text zu Abschnitt 1. Hier kommt alles hin, nichts zusammenfassen!.
[image/test1.jpg]

##Überschrift 2

[image/test2.jpg]
Hier kommt der Text zu Abschnitt 2. Hier kommt alles hin, nichts zusammenfassen!.
[image/test2.jpg]
Hier kommt der Text zu Abschnitt 2.1. Hier kommt alles hin, nichts zusammenfassen!.


##Überschrift 3

Hier kommt der Text zu Abschnitt 3. Hier kommt alles hin, nichts zusammenfassen!.

Transkript:
[{full_transcript_text}]

Wichtige Hinweise:
Länge des Transkripts: Je länger das Transkript, desto mehr Überschriften werden wahrscheinlich benötigt.
Logische Abschnitte: Achte darauf, dass die Überschriften die natürlichen Übergänge und Themenwechsel im Transkript widerspiegeln.
Minimalinvasive Änderungen: Das Ziel ist es, das Transkript zu strukturieren, nicht zu verändern. 
Achte auf den Fließtext und vermeide unnötige Zeilenumbrüche.
"""
                    )
                },
            ],
            options={
                "num_ctx": config.OLLAMA_NUM_CTX,
            }
    

        )
        if response and 'message' in response and 'content' in response['message']:
            script = response['message']['content'].strip()
            if script:
                return script

            else:
                print("Ollama hat einen leeren Abschnitt zurückgegeben.")
                return None
        else:
            print("Unerwartete Antwortstruktur von Ollama:", response)
            return None

    except Exception as e:
        print(f"Ein Fehler bei der Kommunikation mit Ollama ist aufgetreten: {e}")
        return None
    
"""
Example 
# Livestream-Technik: Ein Überblick

Herzlich willkommen zur heutigen Vorlesung. Heute soll es um Livestream-Technik gehen. Da unterteilen wir verschiedene Bereiche: den Bildbereich, den Videobereich, die Lichtbereiche – wie das alles ausgeleuchtet werden muss. Das werden wir in einem schönen Diagramm haben. Das sind die verschiedenen Ebenen. Wir haben natürlich ganz oben das, was man sieht. Das, was man sieht, ist ein Auge. Dann haben wir hier die Kabel und die ganzen Verbindungen und unten haben wir dann Software.

## OBS: Das Tor zum guten Livestream

Wichtig ist auch, dass – das ist ein Zitat von mir – OBS das Tor zum guten Livestream ist.

## Kameras und Anschlüsse

Dann würde ich einmal gerne mit den Kameras anfangen. Genau, hier symbolisch eine Kamera. Also, wir haben verschiedene Möglichkeiten: HDMI-betriebene Kameras, SDI-Kameras, Glasfaser und auch IP, also Ethernet-Kameras. Bei HDMI ist es so, dass wir nur kurze Strecken, aber hohe Bandbreite haben. SDI haben wir sehr lange Strecken und eine etwas niedrigere Bandbreite. Glasfaser hat dann gigantische Strecken und gigantische Bandbreite. Und bei IP-Ethernet haben wir – das ist das Ding – dass man vielleicht noch mit ein paar Latenzen zu kämpfen hat, aber seit dem neuen IB2110-Standard von MacMagic ist das auch schon nicht mehr so wichtig.

[data/cropped/crop1camera4.jpg]

## Kamera-Aufbau: Buddy, Bayonett und Objektive

Genau, wie ist eine Kamera aufgebaut? Wir haben zum einen, das nennt man Buddy. Dieses Buddy ist dann die Kamera mit einem gewissen Bayonet. Und das ist hier das Bayonet. Bayonet. Und da gibt es verschiedene Optionen. Man hat EF-Bayonets, zum Beispiel von Canon. Also hier kann ich hinschreiben: Canon ist gleich EF. Fujifilm hat mehrere. Eins davon ist die XF-Serie. Aber das ist einfach nur der Verschluss für das Objektiv, was dann hier hinkommt. Hier ist das Objektiv.

[data/cropped/crop_0_camera-7.jpg]

"""
