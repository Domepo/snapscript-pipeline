import os
import config
from models.database import init_db
from models.transcript import add_transcript
from models.image_marker import add_image_marker
from services.ollama_service import get_relevant_section
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import images_in_transcript
from utils.text_utils import find_section_end_offset 
from lecture.video_whisper import video_transcript
from lecture.pdf_extractor import convert_pdfs_in_folder



if __name__ == "__main__":
    # video_transcript("data/videos/Download.mp4")
    # transcript_to_script(miaumiau)
    # convert_pdfs_in_folder("data/pdf", "data/lecture_images")
    # get_crop_image("data/lecture_images", "data/cropped", "data/cropped_failed")
    # transcript = images_in_transcript("data/cropped")


    transcript="""Herzlich willkommen zur heutigen Vorlesung.
    Heute soll es um Livestream-Technik gehen.
    Da unterteilen wir verschiedene Bereiche: den Bildbereich, den Videobereich, die Lichtbereiche – wie das alles ausgeleuchtet werden muss.
    Das werden wir in einem schönen Diagramm haben.
    Das sind die verschiedenen Ebenen.
    Wir haben natürlich ganz oben das, was man sieht.
    Das, was man sieht, ist ein Auge.
    Dann haben wir hier die Kabel und die ganzen Verbindungen und unten haben wir dann Software.
    Wichtig ist auch, dass – das ist ein Zitat von mir – OBS das Tor zum guten Livestream ist.
    Dann würde ich einmal gerne mit den Kameras anfangen.
    Genau, hier symbolisch eine Kamera.
    Also, wir haben verschiedene Möglichkeiten: HDMI-betriebene Kameras, SDI-Kameras, Glasfaser und auch IP, also Ethernet-Kameras. 
    Bei HDMI ist es so, dass wir nur kurze Strecken, aber hohe Bandbreite haben.
    SDI haben wir sehr lange Strecken und eine etwas niedrigere Bandbreite.
    Glasfaser hat dann gigantische Strecken und gigantische Bandbreite.
    Und bei IP-Ethernet haben wir – das ist das Ding – dass man vielleicht noch mit ein paar Latenzen zu kämpfen hat, aber seit dem neuen IB2110-Standard von MacMagic ist das auch schon nicht mehr so wichtig.
    Genau, wie ist eine Kamera aufgebaut?
    Wir haben zum einen, das nennt man Buddy.
    Dieses Buddy ist dann die Kamera mit einem gewissen Bayonet.
    Und das ist hier das Bayonet.
    Bayonet.
    Und da gibt es verschiedene Optionen.
    Man hat EF-Bayonets, zum Beispiel von Canon.
    Also hier kann ich hinschreiben: Canon ist gleich EF.
    Fujifilm hat mehrere.
    Eins davon ist die XF-Serie.
    Aber das ist einfach nur der Verschluss für das Objektiv, was dann hier hinkommt.
    Hier ist das Objektiv.
    
    [data/cropped/crop1camera4.jpg]

    [data/cropped/crop_0_camera-7.jpg]

    [data/cropped/crop_0_camera-2.jpg]

    Und an dem Objektiv kann man auch noch Filter dran machen.
    Filter.
    Und da gibt es zum Beispiel UV-Filter.
    Es gibt verschiedenste Filter.
    UV-Filter.
    UV-Filter.
    Wir haben Mistfilter für so einen Glow-Effekt.
    Und es gibt auch noch Variable ND-Filter.
    Darauf komme ich später nochmal.
    Ein Buddy hat auch die Möglichkeit, dass man hier Anschlüsse hat, zum Beispiel ein In-SDI und ein Out-SDI.
    Was dann zu einer CCU geht, wo ich jetzt hin will.
    Und zwar haben wir jetzt eine CCU: eine Camera Control Unit.
    Genau.
    [data/cropped/crop_1_camera-7.jpg]

    [data/cropped/crop_1_camera-6.jpg]

    Also, das ist eine Kamera-Steuerungseinheit.
    Damit lassen sich dann Kameras steuern.
    Das ist zum Beispiel von Blackmagic – so ein Teil hier.
    Hier hat man verschiedene Knöpfe, meistens noch so einen großen Regler, mit dem man hoch- und runter schieben kann, natürlich noch die Program-Knöpfe und Preview-Knöpfe.
    Und dann hat man auch noch verschiedene Texte, hier gibt es Labels.
    Jetzt steht hier Text.
    Text.
    Text.
    Text.
    Und damit ist es dann möglich, zum einen den Fokus, zum einen den Zoom und dann noch verschiedene Bildwerte wie Weißabgleich.   
    Und dann gibt es auch noch die Iris, also die Verblende.
    Dann auch noch Farbkorrekturen, also LUTs nennen wir sie: Look-up-Tables.
    Und die gehen dann gebündelt durch ein Kabel, das ist das SDI Out.
    Weil das ja – ne, das ist – also aus dieser Perspektive ist das SDI Out.
    Und das geht dann in den SDI In.
    Und der SDI Out von der Kamera geht dann in einen Recorder rein, zum Beispiel in einen PC.
    [data/cropped/crop_0_camera-3.jpg]

    Und der schmeißt das dann in OBS.
    [data/cropped/crop_0_camera-4.jpg]

    Was ist OBS?
    Komme ich jetzt zu.
    OBS.
    Das ist die Open Broadcaster Software.
    Und da haben wir zum einen den PC mit einem Record, mit einer Recording-Karte, zum Beispiel auch von Blackmagic, eine Blackmagic 4K-Karte.
    Ist auch eigentlich egal.
    Und da gehen dann die Signale von der CCU – von dem SDI Out rein – der dann ja auch wieder von einem Videomischer kommt.        
    Komme ich nachher zu.
    Und OBS nimmt jetzt dieses Signal, also das ist jetzt sozusagen im PC drin.
    PC.
    Die Verbindung.
    Und dann hat OBS eine schöne Oberfläche, hier hat man die Quellen, hier die Einstellungen und hier den Stream-Start und alles Mögliche.
    Hier kann man das so einstellen, dass man zum einen ein Program und ein Preview hat, also einmal ein Program und ein Preview oder andersrum, kann man noch tauschen, wie man lustig ist.
    Und dadurch kann dieses Signal dann zu YouTube geschickt werden.
    Genau.
    Dann schauen wir uns mal an, was passiert bei YouTube:
    Wir haben die Möglichkeit, diesen Stream bereit zu stellen.
    Gleichzeitig haben wir auch noch Analytics, also wie die Zuschauerzahlen aussehen.
    Dann haben wir auch noch Moderationsfunktionen, darunter Kommentare, Likes, etc.
    Ja.
    Und das alles ist dann recht wichtig, damit man einen Überblick hat, wie ein Stream ankommt.
    [data/cropped/crop_0_camera-1.jpg]

    Genau.
    Und ich habe davor über einen Videomischer geredet, weil wir ja jetzt zum Beispiel mehrere Kameras und Steuerung aller Kameras haben.
    Also machen wir Kamera mal N ist gleich F von X hoch N minus die Wurzel aus YouTube.
    Genau, eine recht einfache Gleichung, aus der folgt natürlich auch, dass E gleich M C Quadrat ist.
    Ne, ganz simpel wegen dem N, was sich jetzt zum E transformiert.
    Und dadurch hat man ja dann auch die Fourier-transformierte der inneren Steigungsfunktion vom Tangentenbeispiel wie bereits gesagt, also das Integral von D von X minus ja 100 100 F Z hoch Pi Cosinus Sinus von X Klammer zu.
    Und das der Videomischer sieht dann wie folgt aus: Man hat hier die Knöpfe hier oben, man hat Knöpfe und dann hat man hier einen Regler, den man hoch oder runter schieben kann, und an dieses Gerät kann man dann Kameras anschließen, die dann auch mit der CCU verbunden werden, wenn wir zum Beispiel mal zwei Kameras haben.
    Genau, und dann braucht das natürlich noch Strom, AC-Strom meistens redundant.
    Und das Ding ist zum Beispiel von Atem von Blackmagic, ein Gerät, ja, so könnte ein Videomischer aussehen.
    Warum machen wir das alles?
    Wir wollen natürlich Zuschauerzeit und wir wollen auch gleichzeitig, dass sich die Bindung erhöht, also dass sich die Zeit, die ein Zuschauer drauf bleibt, erhöht, in Bezug auf die Watchtime.
    Ja, vielen Dank, das war's auch schon.
    """
    # t = transcript_to_script(transcript)
u = """   
    Das ist eine ZUsammenfassung der Vorlesung, die ich heute gehalten habe.
Hier kommt die Zusammenfassung deiner Vorlesung/dokument. Beschreibe knapp, worum es geht.  

## Test
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
video_transcript("data/videos/Download.mp4",config.TRANSCRIPT_PATH)
script = transcript_to_script(config.TRANSCRIPT_PATH)
convert_pdfs_in_folder("data/pdf", "data/lecture_images")
get_crop_image("data/lecture_images", "data/cropped", "data/cropped_failed")
images_in_transcript("data/cropped", config.FULL_TRANSCRIPT_TEXT)
keywords = create_keywords(script)
create_typst_document(script, keywords)