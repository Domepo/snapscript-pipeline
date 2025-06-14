import os
import config
import json
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import images_in_transcript,compare_image_text_timestamp
from controllers.video_whisper import generate_transcript, store_transcript
from models.database import init_db
from utils.token_count import count_tokens
from utils.video_to_image_timestamp import extract_frames_rename_by_timestamp

script_ma = """
# Das Zweikörperproblem und Kepler'sche Gesetze

Dieses Transkript behandelt das Zweikörperproblem in der Physik, die Herleitung von Kepler'schen Gesetzen und die Berechnung der Fluchtgeschwindigkeit. Es werden sowohl theoretische Grundlagen als auch praktische Anwendungen diskutiert, wobei auf die Energieerhaltung und den Drehimpulserhaltungssatz eingegangen wird.

## Herleitung der Bewegungsgleichungen und Vereinfachungen

Zweikörperproblem und die aufgespaltene Gleichung würde ich jetzt gerne noch einmal hinschreiben für die x-Komponente.
Also das hatten wir auf der anderen auch schon mal stehen einmal.
Und dann ist das x-Zweipunkt ist gleich minus g Groß M plus Klein M durch R hoch 3 mal x.
Wenn Sie diese Differenzialgleichung lösen, brauchen Sie natürlich nicht nur die eine, sondern alle drei.
Wir wollen ja alle Raumkomponenten wissen.
Brauchen Sie insgesamt sechs Integrationen.
Um diese Integration zu machen, müssen Sie keine Vereinfachung machen, aber Sie müssen bestimmte Erhaltungssätze in der Physik nutzen.
Und das ist jetzt quasi die größte Vereinfachung, die wir hier machen.
Nämlich, das machen wir nicht hier.
Ich habe das schon gesagt, das ist relativ langwierig.
Aber Sie können mir glauben, dass die Ergebnisse, die ich Ihnen gleich zeige, davon erstmal soweit richtig sind.
Wenn Sie das nachlesen möchten, können Sie in jedes beliebige Buch schauen, was irgendwie so heißt.
Theoretische Physik, klassische Mechanik.
Ein Beispiel wäre da der sogenannte Nolting.
Das ist eine ganze Reihe.
Ich glaube, sieben oder acht Bände von was fürs Nachttischchen.

## Bewegung in einer Ebene und Drehimpulserhaltung

Wichtige Sache, wofür wir vielleicht das erste Experiment brauchen, ist, wenn Sie die Impulserhaltung nutzen, dann stellen Sie fest, die Bewegung eines Planeten erfolgt in einer Ebene.
Oder anders, man muss es sagen, die Bewegung dieser beiden Körper sind immer in einer Ebene.
Wenn wir das jetzt einfach versuchen, irgendwie zu skizzieren, das ist natürlich relativ naheliegend, wie das aussieht.
Das soll jetzt irgendwie diese Ebene sein.
Und Ihre beiden Körper umwandern sich hier also quasi innerhalb dieser Ebene und können die Ebene in die Plus-Minus-Richtung nach oben und unten nicht verlassen.
Wenn Sie das berechnen, finden Sie dann folgendes.
Das Flächenelement DA, zeige ich Ihnen gleich kurz, wo Sie ein A finden, ein Halb L durch M mal DT ist.
Dabei ist DA ein Flächenelement, L ist der sogenannte Systemdrehimpuls, M ist die Masse des kleinen Körpers und DT ist ein Zeitelement.

## Flächensatz und Kepler's Zweites Gesetz

So, wenn wir das jetzt auf das Kleine beziehen, wie wir das gerade gemacht haben, könnten wir das ungefähr so einzeichnen.
Wir tun jetzt mal einfach so, als wenn hier der Brennpunkt ist oder der Schwerpunkt in dem Fall.
Und dann könnten Sie sich hier vorstellen, das war der Radiusvektor zum Punkt T1.
Das ist der Radiusvektor zum Punkt T2.
Und hier drin haben Sie jetzt eine Fläche A1.
Und wenn Sie sich in diesem System ein kleines Flächenelement mit einem Delta T einfach nur vorstellen, dann würden Sie sehen, okay, ein sehr, sehr kleines Stück hiervon hat jetzt die Breite DT und die Fläche DA.
Also wenn Sie später integrieren, dann integrieren Sie immer über solche Kreise.
Und jetzt zeigt sich in der Physik, dass der Drehimpuls eine Erhaltungsgröße ist.
So, das heißt, wenn Sie in einem System einen Drehimpuls haben und Sie haben keine äußere Kraft auf dieses System und wenn sich zwei Körper im luftleeren Raum umkreisen, haben Sie relativ wenig äußere Kräfte.  
Also wenn man alle anderen Planeten und Massen sich wegdenkt, dann ist der Drehimpuls eine Erhaltungsgröße.
Und dafür gibt es ein sehr, sehr schönes Demonstrationsexperiment.
Wenn wir jetzt sehen, dass der Drehimpuls eine Erhaltungsgröße ist, dann stellen Sie fest, dass das L konstant ist.
Das M ist konstant, die Masse verändert sich ja nicht unterwegs, da schmeißt ja keiner was runter.
Das 1,5 ist sowieso konstant und dann folgt direkt daraus eine Proportionalität zwischen DA und DT.
[data/cropped/197166.jpg]
Und das ist das zweite Kepler'sche Gesetz.
Und wenn Sie das ausformulieren, dann heißt das, das hört sich jetzt etwas anders an, aber es heißt tatsächlich so, der Radiusvektor überstreicht in gleichen Zeiten gleiche Flächen.
Und wenn wir das nochmal aufmalen, dann ist das wieder die Ellipse mit dem Schwerpunkt im Brennpunkt hier.
Wir haben hier, obwohl die Massen brauchen wir jetzt gar nicht mehr, wir brauchen nur noch die Radiusvektoren.
Wir nehmen jetzt hier genau das gleiche wie eben.
Das ist der Radiusvektor zum Zeitpunkt T1 und Zeitpunkt T2 und diese Fläche ist dann A1.
Und wenn wir das jetzt hier ein bisschen weiter weg machen für das andere, dann sieht das ungefähr so aus.
Das hier soll jetzt der Zeitpunkt T3 sein, das soll der Zeitpunkt T4 sein und diese Fläche ist A2.
Und wenn Sie sich das klar machen, was oben steht, dann steht da folgendes.
T4 minus T3, das ist also ein Delta T.
Wenn das genauso groß ist wie T2 minus T1, also von T1 nach T2 zu den Positionen brauchst genauso lange wie von T3 nach T4, dann folgt daraus, dass die Fläche A1 genauso groß ist wie die Fläche A2.
Und das sagt im Prinzip der Satz.
Der Radiusvektor überstreicht in gleichen Zeiten, also dt1 gleich dt2, gleiche Flächen A1 gleich A2.
Und das hat der Kepler herausgefunden, indem er Daten ausgewertet hat, die von Tycho Bra gesammelt wurden.
Und das konnte er dann quasi, ohne dass er wusste, wie man dieses Zweikörperproblem löst, ausrechnen.

## Die Lösung des Zweikörperproblems und Kegelschnitte

So, wenn Sie das Ganze wirklich komplett lösen, also der nächste Schritt ist, Sie machen noch eine Integration mit der Energiehaltung und noch was und noch was,
[data/cropped\298800.jpg]
dann führt das darauf, dass Sie folgende Gleichungen erhalten.
Also die echte Lösung für den Radiusvektor sieht so aus.
R in Abhängigkeit vom Winkel ist gleich P geteilt durch 1 plus E mal Cosinus Theta.
Und das ist ein Kegelschnitt.
So, wenn wir jetzt angucken, dabei sind P und E beides Konstanten, die vom jeweiligen System abhängen.
Da stecken dann irgendwelche Massen und so drin.
Also es ist jetzt nicht wichtig, dass man genau weiß, welche anderen Größen da drin stecken.
Es ist wichtig nur, dass sie konstant sind.
Und E ist eine besondere Konstante, das heißt, die hat auch einen eigenen Namen.
Das ist die sogenannte numerische Exzentrität.
Exzentrität.
Diese numerische Exzentrität, die können wir tatsächlich ändern.
Also R ist in diesem Fall, wenn wir uns jetzt eine kleine Ellipse hier hinzeichnen
und hier jetzt irgendwie unseren Schwerpunkt oder Brennpunkt haben, je nachdem,
dann ist das hier das R.
Und man fängt halt an irgendeiner Stelle an, muss man in 0 festlegen
und dann hätte man hier den Winkel Theta.
Also Theta geht von 0 bis 360 Grad und dann kriegt man immer dann die Ellipse raus.

## Abhängigkeit der Bahnform von der Geschwindigkeit

Komma, das haben wir auch schon gesehen.
Wenn die numerische Exzentrität 1 ist, gibt es eine Ellipse.
So, und jetzt ist die Frage, was kann man davon ändern?
Das P ist für uns fest.
Das ist auf jeden Fall eine Konstante, die wir nicht ändern können.
Aber die numerische Exzentrität, auf die haben wir Einfluss, denn da steckt die Geschwindigkeit mit drin.
Und jetzt könnte man sich auf folgenden Aufbau überlegen.
Und zwar nehmen wir an, das soll die Erde sein.
Oder halt irgendein Planet.
Oder irgendeine Masse, das würde reichen.
Auf diese Masse bauen wir jetzt einen sehr, sehr hohen Turm.
Wir sehen, wie hoch der ist.
So, und auch von diesem Turm werfen wir jetzt eine andere kleine Masse weg.
Und zwar soll diese Masse eine Geschwindigkeit V haben.
Und die soll, ich mache da jetzt eine Parallelverschiebung, einfach nur in diese Richtung gehen.
Das heißt, wir werfen die parallel zur Erdoberfläche und senkrecht zum Turm quasi seitlich weg.
Und jetzt gibt es unterschiedliche Möglichkeiten.
Wenn Sie die Kegelschnitte lösen, dann können wir sagen, okay, wenn wir nur ganz locker werfen.
Das ist so das, was unser tägliches Leben ist.
Ja, also wenn Sie von irgendeinem Turm irgendwas runterwerfen, dann kommt das meist nicht wieder irgendwann bei Ihnen an.
Sondern es passiert Folgendes.
Sie werfen das runter und es kracht hier auf den Boden.
Ja, dieser Fall 1 ist eine Parabel.
[data/cropped\438766.jpg]
[data/cropped\438767.jpg]
So, den Fall 2, den nehmen wir jetzt.
Da werfen Sie jetzt richtig, richtig feste.
Also übrigens muss dieser Turm so hoch sein, dass keine Atmosphäre mehr stört.
Sonst funktioniert das nicht.
Und wenn Sie jetzt so feste werfen, dann kann Ihnen folgendes passieren, dass Sie einen Kreis erzeugen.
Also das ist jetzt der Fall 2.
Da haben Sie schon so feste geworfen, dass Sie genau einen Kreis erzeugen.
Und den einzigen Unterschied, den Sie gemacht haben, das ist nur die Geschwindigkeit.
Jetzt erhöhen Sie die Geschwindigkeit noch weiter.
Dann passiert Folgendes.
Das sieht am Anfang so ein bisschen ähnlich aus.
Aber Sie erzeugen eine Ellipse.
Also der Fall 3 mit noch höherer Geschwindigkeit ist eine Ellipse.
Aber Sie sind immer noch gebunden.
Das heißt, wir sind immer noch egal, wie feste Sie werfen.
Also solange Sie bei 3 sind, kommt der Ball oder die Masse immer wieder bei Ihnen an.
Hat aber auf der anderen Seite eine viel größere Entfernung, als der Turm hoch ist.
Und dann können Sie noch die Variante 4 machen.
Das ist jetzt, wenn Sie noch schneller werfen, dann wird aus dem Ganzen eine Hyperbel.
So, wenn Sie das gemacht haben, dann verlassen Sie den Einflussbereich des Planeten.
Das heißt, der Unterschied zwischen Parabel, Kreis, Ellipse und Hyperbel steuern Sie mit der Geschwindigkeit.

## Fluchtgeschwindigkeit und Energieerhaltung

Und jetzt möchte man natürlich zumindest wissen, letztendlich, welche Geschwindigkeit brauchen Sie, um zum Beispiel der Erde zu entfliehen.
Also die sogenannte Fluchtgeschwindigkeit.
Um das zu berechnen, müssen wir uns jetzt einmal anschauen, wie viel Energie überhaupt in dieser Bewegung um einen Schwerpunkt drin steckt.
Und wenn Sie jetzt nämlich die Energie in diesem System berechnen, dann hält man relativ einfach.
Und zwar wichtig, in dem Fall machen wir das nur für den kleinen Körper.
Der große oder der andere könnte man das alles äquivalent machen, aber wir wollen es erstmal nur für den kleinen Körper machen.
Und zwar die Gesamtenergie.
Ey, Gesamt ist nichts anderes als die beiden einzigen Energien, die wir haben.
Das ist einmal die kinetische Energie plus die potenzielle Energie.
Beide von diesen Energieformen kennen wir.
Das ist einmal gleich 1,5 mv² und minus g mal M mal m durch r.
So, achten Sie darauf, sonst in der Kraft war immer r², in der Energie ist nur noch durch r.
Und weil wir die Energieerhaltung kennen, können wir direkt sagen, dass das Ganze auf jeden Fall eine Konstante ist.
Solange in unserem System keine Energie nach außen abfließt, was wir ausschließen wollen.
Direkt daraus kann man schon eine Folgerung ziehen.
Und zwar, wenn die Bahn fest ist, das ist jetzt das Wichtige, dann ist ein leichterer Körper, muss schneller sein als ein schwererer Körper.
Das ist natürlich nicht verwunderlich, das hätten wir über den Kraftansatz genauso rausgekriegt.
Aber wenn man jetzt einen kompletten Umlauf sich betrachtet, also Sie betrachten das für alle Winkel, Theta von 0 bis 360 Grad,
und macht dann den Mittelwert, dann erhält man eine interessante Beziehung, und zwar den sogenannten Viralsatz.
Und zwar ist der Mittelwert der kinetischen Energie betragsmäßig genau die Hälfte vom Mittelwert der potenziellen Energie.
Das ist in klassische Mechanik.
So, weil das ein wichtiger Satz ist, schreiben wir das nochmal auf.
Das zeitliche Mittel der kinetischen Energie entspricht betragsmäßig dem zeitlichen Mittel der halben potenziellen Energie.
Und diesen Zusammenhang, den nutzen wir jetzt aus, um letztendlich die Bahngeschwindigkeit zu bestimmen.
Und dazu schauen wir uns jetzt auf der Bahn zwei ganz spezielle Punkte an.
Also um diese Geschwindigkeit zu bestimmen, was dann ziemlich einfach ist, geht man wie folgt vor.
Und zwar schaut man sich einfach einmal wieder die Energie an, die wir vorher schon hatten.
Und zwar 1 halb m V Quadrat für das Teilchen Minus Groß G, Klein M, Groß M durch R.
Und davon wussten wir vorher nur, das ist die Gesamtenergie des Systems, aber die kennen wir jetzt auch.
Denn die Gesamtenergie ist Minus Groß M, Klein M, Groß M geteilt durch 2A.
[data/cropped/1001733.jpg]
So, wenn wir jetzt einfach wissen, dass dieser Term 0 wird, dann setzen wir das einfach ein und erhalten die Fluchtgeschwindigkeit.
Also V-Flucht muss größer gleich der Wurzel aus 2 Groß G Groß M durch R sein.
Also für die Erde ist diese Geschwindigkeit 11,2 Kilometer pro Sekunde.
"""
key = '["Zweikörperproblem", "Kepler", "Energieerhaltung", "Bewegung", "Fluchtgeschwindigkeit", "Bahn", "Gravitation"]'

if __name__ == "__main__":
    print("Starte den Prozess...")
    init_db()

    # script = generate_transcript("data/videos/Astro.mp4")
    # transcript_id = store_transcript(script, config.TRANSCRIPT_PATH)

    # extract_frames_rename_by_timestamp("data/videos/Astro.mp4", "data/tmp")

    """
    Change token count to run the model faster.
    """
    # config.OLLAMA_NUM_CTX = count_tokens(config.FULL_TRANSCRIPT_TEXT)


    ### get_crop_image("data/tmp", "data/cropped", "data/cropped_failed")
    
    script_with_images = compare_image_text_timestamp("data/cropped", 6,"data/transcript/transcript_with_images.txt")
    # config.OLLAMA_NUM_CTX = count_tokens(script_with_images)


    # print(script_with_images)
    script_with_images = images_in_transcript("data/cropped", config.FULL_TRANSCRIPT_TEXT)
    # print(script_with_images)
    script = transcript_to_script(script_with_images)

    config.OLLAMA_NUM_CTX = count_tokens(script_ma)

    print(script_ma)

    # keywords = create_keywords(script)
    # print(keywords)
    create_typst_document(script_ma, key)