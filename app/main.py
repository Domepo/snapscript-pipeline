import os
import config
import json
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script_iterative
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import images_in_transcript,compare_image_text_timestamp
from controllers.video_whisper import generate_transcript, store_transcript
from models.database import init_db
from utils.token_count import count_tokens
from utils.video_to_image_timestamp import extract_frames_rename_by_timestamp

script_ma = """
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
Eine wichtige Sache, wofür wir vielleicht das erste Experiment brauchen, ist, wenn Sie die Impulserhaltung nutzen, dann stellen Sie fest, die Bewegung eines Planeten erfolgt in einer Ebene.
Oder anders, man muss es sagen, die Bewegung dieser beiden Körper sind immer in einer Ebene.
Wenn wir das jetzt einfach versuchen, irgendwie zu skizzieren, das ist natürlich relativ naheliegend, wie das aussieht.
Das soll jetzt irgendwie diese Ebene sein.
Und Ihre beiden Körper umwandern sich hier also quasi innerhalb dieser Ebene und können die Ebene in die Plus-Minus-Richtung nach oben und unten nicht verlassen.
Wenn Sie das berechnen, finden Sie dann folgendes.
Das Flächenelement DA, zeige ich Ihnen gleich kurz, wo Sie ein A finden, ein Halb L durch M mal DT ist.
Dabei ist DA ein Flächenelement, L ist der sogenannte Systemdrehimpuls, M ist die Masse des kleinen Körpers und DT ist ein Zeitelement.
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
So, wenn Sie das Ganze wirklich komplett lösen, also der nächste Schritt ist, Sie machen noch eine Integration mit der Energiehaltung und noch was und noch was und noch was,
[data/cropped/298800.jpg]
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
Also R ist in diesem Fall, wenn wir uns jetzt nochmal so eine kleine Ellipse hier hinzeichnen
und hier jetzt irgendwie unseren Schwerpunkt oder Brennpunkt haben, je nachdem,
dann ist das hier das R.
Und man fängt halt an irgendeiner Stelle an, muss man in 0 festlegen
und dann hätte man hier den Winkel Theta.
Also Theta geht von 0 bis 360 Grad und dann kriegt man immer dann die Ellipse raus.
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
[data/cropped/438766.jpg]
[data/cropped/438767.jpg]
So, den Fall 2, den nehmen wir jetzt.
Da werfen Sie jetzt richtig, richtig feste.
Also übrigens muss dieser Turm so hoch sein, dass keine Atmosphäre mehr stört.
Sonst funktioniert das nicht.
Und wenn Sie jetzt so feste werfen, dann kann Ihnen Folgendes passieren, dass Sie einen Kreis erzeugen.
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
Das heißt, den Unterschied zwischen Parabel, Kreis, Ellipse und Hyperbel steuern Sie mit der Geschwindigkeit.
So, und jetzt möchte man natürlich zumindest wissen, letztendlich, welche Geschwindigkeit brauchen Sie, um zum Beispiel der Erde zu entfliehen.
Also die sogenannte Fluchtgeschwindigkeit.
Um das zu berechnen, müssen wir uns jetzt einmal anschauen, wie viel Energie überhaupt in dieser Bewegung um einen Schwerpunkt drin steckt.
[data/cropped/527366.jpg]
[data/cropped/527367.jpg]
Und wenn Sie jetzt nämlich die Energie in diesem System berechnen, dann hält man relativ einfach.
Und zwar wichtig, in dem Fall machen wir das nur für den kleinen Körper.
Der große oder der andere könnte man das alles äquivalent machen, aber wir wollen es erstmal nur für den kleinen Körper machen.
Und zwar die Gesamtenergie.
Ey, Gesamt ist nichts anderes als die beiden einzigen Energien, die wir haben.
Das ist einmal die kinetische Energie plus die potenzielle Energie.
Beide von diesen Energieformen kennen wir.
Das ist einmal gleich 1,5 mv² und minus g mal M mal m durch r.
So, achten Sie darauf, sonst in der Kraft war immer r², in der Energie ist nur noch durch r.
Und weil wir ja die Energieerhaltung kennen, können wir direkt sagen, dass das Ganze auf jeden Fall eine Konstante ist.
Solange in unserem System keine Energie nach außen abfließt, was wir ausschließen wollen.
Direkt daraus kann man schon eine Folgerung ziehen.
Und zwar, wenn die Bahn fest ist, das ist jetzt das Wichtige, dann ist ein leichterer Körper, muss schneller sein als ein schwererer Körper.
Das ist natürlich nicht verwunderlich, das hätten wir über den Kraftansatz genauso rausgekriegt.
Aber wenn man jetzt quasi einen kompletten Umlauf sich betrachtet, also Sie betrachten das für alle Winkel, Theta von 0 bis 360 Grad,
und macht dann den Mittelwert, dann erhält man eine interessante Beziehung, und zwar den sogenannten Viralsatz.
Und zwar ist der Mittelwert der kinetischen Energie betragsmäßig genau die Hälfte vom Mittelwert der potenziellen Energie.
Also die Herleitung finden Sie auch, klassische Mechanik.
So, weil das ein wichtiger Satz ist, schreiben wir das nochmal auf.
Das zeitliche Mittel der kinetischen Energie entspricht betragsmäßig dem zeitlichen Mittel der halben potenziellen Energie.
Und diesen Zusammenhang, den nutzen wir jetzt aus, um letztendlich die Bahngeschwindigkeit zu bestimmen.
Und dazu schauen wir uns jetzt auf der Bahn zwei ganz spezielle Punkte an.
Also um diese Geschwindigkeit zu bestimmen, muss man als allererstes rauskriegen, was ist die quantitative Gesamtenergie.
Das heißt, bisher ist es klar, dass es eine Konstante ist, die Gesamtenergie.
Aber wie hoch diese Konstante ist, das schauen wir uns jetzt an.
Und zwar nutzen wir dazu die Energie am sogenannten Perihail.
Das ist einfach nichts anderes als den Punkt, wo der Schwerpunkt und der Körper am nächsten zusammen sind.
Vielleicht zeichnen wir das einmal kurz auf.
Also wenn wir das jetzt übertreiben, dann ist das hier der Schwerpunkt.
Das hier ist die Masse.
Und einen halben Umlauf später ist die Masse hier.
Und dann ist das hier der nächste Punkt, das sogenannte Perihail.
Und jetzt gleich kommt als nächstes die Energie am Abhehl.
Das ist natürlich dann der Punkt, der am weitesten weg ist vom Schwerpunkt.
Und da können Sie immer darauf achten, dass diese Linie, die jetzt die beiden Massen zu unterschiedlichen Zeitpunkten und den Schwerpunkt verbinden,
das ist immer zweimal die große Halbachse.
Das brauchen wir später nochmal.
Okay, um das vielleicht ein bisschen genauer zu machen hier, das ist vielleicht eher, ja ich habe es schon verbockt,
das wäre in dem Fall eigentlich eher hier, wäre der Schwerpunkt vermutlich in dem System.
Also das Perihail ist tatsächlich nur einmal da und das gibt es nur an der Stelle.
So und jetzt schauen wir uns da einmal die entsprechenden Energien an.
Und zwar gilt an der Stelle, dass die Energie E0, das ist jetzt die Gesamtenergie, die wir noch nicht kennen,
die soll jetzt am Perihail sein, 1 halb m Geschwindigkeit am Perihail zum Quadrat,
minus Groß G, Klein M, Groß M geteilt durch den Radius am Perihail.
So, diese Gleichung nehmen wir jetzt mal dem Abstand am Perihail, also RP zum Quadrat und dann erhalten wir E0,
RP Quadrat ist gleich 1 halb m, VP Quadrat, RP Quadrat, minus G, Klein M, Groß M, mal RP.
Das ist jetzt gleich Gleichung 1 und auf der anderen Seite schauen wir uns das gleiche an.
Auch hier ist die Energie E0, weil die Gesamtenergie ja gleich groß sein muss, Energieerhaltung.
Und wenn wir das aufschreiben, ist das 1 halb m, V abheilt zum Quadrat, minus Groß G, Klein M, Groß M durch R abheilt.
Und auch hier machen wir jetzt das gleiche, wir multiplizieren das mit RP zum Quadrat.
Dann kommt da folgendes raus, E0, RP Quadrat gleich 1 halb m, V abheilt Quadrat, RP Quadrat, minus Groß G, Klein M, Groß M, mal RP ohne Quadrat.
Diese Gleichung nennen wir 2.
Und jetzt kommt eine kleine Zwischenfolgerung, die wir machen.
Und zwar, wenn wir uns daran erinnern, dass der Drehimpuls erhalten bleibt, können wir folgendes machen.
Und zwar gilt VA, also die Geschwindigkeit am Abheil, mal der Radius am Abheil muss genauso groß sein wie die Geschwindigkeit, also VP am Perihil, mal RP.
Und wenn das richtig ist, dann gilt genauso, dass 1 halb m, V, P Quadrat, RP Quadrat das gleiche ist wie 1 halb m, V, A Quadrat, RA Quadrat.
Und um jetzt tatsächlich eine Vereinfachung zu erzielen, machen wir eine Subtraktion.
Das heißt, wir wollen folgendes berechnen, und zwar Gleichung 2 minus Gleichung 1.
Und dann sehen Sie, was da passiert.
Wir machen erstmal die linken Seiten.
Das ist noch ziemlich einfach.
Da steht dann nämlich nichts anderes als E0, RA Quadrat minus E0, RP Quadrat.
Dann kommt das Gleichheitszeichen.
Jetzt haben wir festgestellt, dass 1 halb m, VP Quadrat, RP Quadrat das gleiche ist wie 1 halb m, VA Quadrat, RA Quadrat.
Damit kürzen sich jetzt die kinetischen Terme, na sie kürzen sich nicht weg, aber sie subtrahieren sich raus, weil sie genau gleich sind.
Das heißt, die brauchen wir nicht beachten.
Und dann bleiben nur noch die Gravitationsterme über.
Da klammern wir jetzt direkt mal minus Groß M, Klein M, Groß G aus.
Und dann haben wir da stehen, Minus Groß G, Klein M, Groß M, mal ein Bruch.
Und in dem Bruch steht nur noch RA minus RP, geteilt durch RA Quadrat minus RP Quadrat.
Und das können wir jetzt noch etwas vereinfachen.
Und zwar wie folgt.
Genau, genau.
Also bei dieser Gleichung, die ist jetzt noch verkehrt.
Denn, was ich eigentlich gemacht habe, ist, ich habe noch durch...
Ne, das machen wir anders.
Das machen wir schön.
Also wir radieren das wieder weg und machen das in zwei Schritten.
Dann steht da nämlich im ersten Schritt nur RA minus RP.
Und jetzt klammern wir auf der einen Seite E0 aus.
Dann steht da E0 mal Klammer auf RA Quadrat minus RP Quadrat.
Und das teilen wir dann durch die andere Seite.
Und dann bleibt hier nur noch stehen, E0 ist gleich Minus Groß M, Klein M, Groß M.
Und dann kommt der Bruch mit dem Zähler RA minus RP und dem Nenner RA Quadrat minus RP Quadrat.
So, wenn Sie sich den Nenner anschauen, dann sehen Sie direkt, aha, das ist sowas wie eine binomische Formel.
Und wenn wir die auflösen, haben wir RA minus RP mal RA plus RP.
Und dann sehen Sie, aha, eins kürzt sich davon dankenswerterweise raus, sodass am Ende nur noch überbleibt.
Minus Groß G, Klein M, Groß M, geteilt durch RA plus RP.
Und wenn wir jetzt noch ganz kurz schauen in die Skizze, die wir oben gemacht haben, dann stellen wir folgendes fest, dass das hier ja RA ist.
Und dieses kleine Stück RP ist, kein V, das soll ein R sein, ich schreibe das neu, RP.
Und dann sehen Sie, dass folgendes gilt, die doppelte große Halbachse ist die Summe aus RA und RP.
Und dann vereinfacht sich das Ganze noch zu Minus Groß G, Klein M, Groß M durch 2A.
So, damit haben wir E0 bestimmt.
Das heißt, die Gesamtenergie in diesem kompletten System für die eine Masse ist Minus Groß G, Klein M, Groß M, geteilt durch 2A.
[data/cropped/1001733.jpg]
So, wenn man dann nämlich jetzt die Bahngeschwindigkeit ausrechnen möchte, was dann ziemlich einfach ist, geht man wie folgt vor.
Und zwar schaut man sich einfach einmal wieder die Energie an, die wir vorher schon hatten.
Und zwar 1,5m V Quadrat für das Teilchen Minus Groß G, Klein M, Groß M durch R.
Und davon wussten wir vorher nur, das ist die Gesamtenergie des Systems, aber die kennen wir jetzt auch.
Denn die Gesamtenergie ist Minus Groß M, Klein M, Groß M geteilt durch 2A.
So, das löst man dann einfach nach V auf.
Das geht auch in einem Schritt.
Und dann steht da nichts anderes als eine große Wurzel.
Und in dieser Wurzel steht 2 mal Groß M, Groß G und dann in der Klammer 1 durch R minus 1 durch 2A.
Und das ist die Bahngeschwindigkeit in Abhängigkeit des Radiusvektors.
Denn der Rest ist für ein System konstant.
Und wenn wir uns jetzt überlegen, jetzt denken wir nochmal zurück an den Wurf von unserem hohen Turm.
Wie groß müsste denn jetzt die Geschwindigkeit sein, um dem schwere Feld eines Körpers zu entrinnen?
Also quasi das M ist eine, also wir haben eine kleine Kugel in der Hand.
Und wie schnell müssen wir jetzt werfen, dass eine Hyperbel entsteht?
Das heißt, sie nicht wieder offen ist.
Und im Grenzübergang ist eine Hyperbel nichts anderes als eine Ellipse mit einer unendlichen Halbachse.
Da sehen Sie, was passiert.
Wenn wir nämlich das A unendlich groß machen, wird die Gesamtenergie 0.
Das heißt, unser Teilchen ist ungebunden.
Also das könnte man hier noch vorschreiben.
E Gesamt, dass das konsistent ist, ist da gleich 0.
Da beim Grenzübergang für A gegen unendlich von Minus Groß G Klein M Groß M durch 2A eine 0 rauskommt.
Wenn wir jetzt einfach wissen, dass dieser Term 0 wird, dann setzen wir das einfach ein und erhalten die Fluchtgeschwindigkeit.
Also um eine solche Bahn, eine Hyperbel zu erreichen, ist dann diese Geschwindigkeit nötig.
Und diese Geschwindigkeit wird Fluchtgeschwindigkeit genannt.
Also V-Flucht muss größer gleich der Wurzel aus 2 Groß G Groß M durch R sein.
Also für die Erde ist diese Geschwindigkeit 11,2 Kilometer pro Sekunde.
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
    
    # script_with_images = compare_image_text_timestamp("data/cropped", 6,"data/transcript/transcript_with_images.txt")
    # config.OLLAMA_NUM_CTX = count_tokens(script_with_images)


    # print(script_with_images)
    # script_with_images = images_in_transcript("data/cropped", config.FULL_TRANSCRIPT_TEXT)
    # print(script_with_images)
    # script = transcript_to_script_iterative(script_ma)

    # config.OLLAMA_NUM_CTX = count_tokens(script_ma)

    # print(script_ma)
    aaa = """
    # Das Zweikörperproblem und Bahnberechnungen

    Dieses Skript behandelt das Zweikörperproblem und dessen Lösungen, beginnend mit der Herleitung der Drehimpulserhaltung und deren Auswirkungen auf die Bewegung der Körper. Es wird gezeigt, wie sich aus der Erhaltung des Drehimpulses Keplersche Gesetze ableiten lassen, insbesondere das zweite Keplersche Gesetz, das die Flächengleichheit in gleichen Zeiten beschreibt. Die Vorlesung behandelt Kegelschnitte als Lösungen der Bewegungsgleichungen, wobei die numerische Exzentrizität die Art der Bahn bestimmt (Parabel, Kreis, Ellipse, Hyperbel). Abschließend wird die Berechnung der Bahngeschwindigkeit und die Herleitung der Fluchtgeschwindigkeit anhand von Energiebetrachtungen und der Drehimpulserhaltung dargelegt. Die Fluchtgeschwindigkeit wird für die Erde mit etwa 11,2 km/s angegeben.

    ## Das Zweikörperproblem und der Drehimpulserhaltungssatz

    Beginnen wir mit der Aufschreibung der x-Komponente der Gleichung für das Zweikörperproblem. Wir hatten dies bereits einmal betrachtet. Die Gleichung lautet: x-Doppelpunkt ist gleich minus g Groß M plus Klein M durch R hoch 3 mal x. Um diese Differentialgleichung zu lösen, benötigen Sie nicht nur diese eine, sondern alle drei Raumkomponenten, also insgesamt sechs Integrationen. Diese Integrationen erfordern keine Vereinfachungen, sondern die Anwendung bestimmter Erhaltungssätze aus der Physik. Dies stellt im Grunde die größte Vereinfachung dar, die wir hier vornehmen. Ich habe bereits erwähnt, dass dies relativ zeitaufwändig ist, aber Sie können darauf vertrauen, dass die Ergebnisse, die ich Ihnen gleich zeige, zunächst korrekt sind. Wenn Sie dies nachlesen möchten, finden Sie Informationen in jedem Lehrbuch über theoretische Physik oder klassische Mechanik. Ein Beispiel wäre der Nolting, eine umfassende Reihe in sieben oder acht Bänden.

    Ein wichtiger Punkt, für den wir möglicherweise das erste Experiment benötigen, ist, dass die Impulserhaltung die Bewegung eines Planeten auf eine Ebene beschränkt. Oder anders ausgedrückt, die Bewegung der beiden Körper findet immer in einer Ebene statt. Stellen wir uns dies als Skizze vor: Es handelt sich um diese Ebene. Die beiden Körper umkreisen einander innerhalb dieser Ebene und können diese in der Plus-Minus-Richtung nach oben oder unten nicht verlassen. Bei der Berechnung finden Sie, dass das Flächenelement DA gleich einem halben L durch M mal DT ist. Hierbei ist DA ein Flächenelement, L der Systemdrehimpuls, M die Masse des kleinen Körpers und DT ein Zeitelement.

    Wenn wir dies nun auf den kleinen Körper beziehen, wie wir es gerade getan haben, können wir uns das wie folgt vorstellen: Nehmen wir an, der Brennpunkt oder Schwerpunkt befindet sich hier. Dann können Sie sich vorstellen, dass dies der Radiusvektor zum Punkt T1 und dies der Radiusvektor zum Punkt T2 ist. Hier haben Sie eine Fläche A1. Wenn Sie sich in diesem System ein kleines Flächenelement mit einem Delta T vorstellen, würden Sie sehen, dass ein sehr kleines Stück hiervon die Breite DT und die Fläche DA hat. Wenn Sie später integrieren, integrieren Sie immer über solche Kreise.

    In der Physik zeigt sich, dass der Drehimpuls eine Erhaltungsgröße ist. Das bedeutet, wenn Sie in einem System einen Drehimpuls haben und keine äußeren Kräfte auf dieses System wirken, dann ist der Drehimpuls konstant. Wenn sich zwei Körper im luftleeren Raum umkreisen, gibt es relativ wenig äußere Kräfte. Wenn man alle anderen Planeten und Massen weggedacht werden, ist der Drehimpuls eine Erhaltungsgröße. Es gibt ein sehr schönes Demonstrationsexperiment dafür.

    Da der Drehimpuls eine Erhaltungsgröße ist, ist L konstant. Die Masse M ist ebenfalls konstant, da sich die Masse unterwegs nicht ändert. Da 1,5 konstant ist, folgt direkt eine Proportionalität zwischen DA und DT.

    [data/cropped/197166.jpg]

    ## Das Zweite Keplersche Gesetz

    Das zweite Keplersche Gesetz besagt, dass der Radiusvektor in gleichen Zeiten gleiche Flächen überstreicht. Betrachten wir eine Ellipse mit dem Schwerpunkt im Brennpunkt. Wir benötigen hierbei keine Massen mehr, sondern lediglich die Radiusvektoren zu verschiedenen Zeitpunkten. Nehmen wir an, wir haben einen Radiusvektor zum Zeitpunkt T1 und einen weiteren zum Zeitpunkt T2, die eine Fläche A1 einschließen. Betrachten wir nun einen Radiusvektor zum Zeitpunkt T3 und einen weiteren zum Zeitpunkt T4, die eine Fläche A2 einschließen.

    Wenn die Zeitdifferenz zwischen T1 und T2 genauso groß ist wie die zwischen T3 und T4 – also ΔT1 = ΔT2 – dann folgt daraus, dass die Fläche A1 genauso groß ist wie die Fläche A2. Im Wesentlichen besagt der Satz also, dass der Radiusvektor in gleichen Zeiten gleiche Flächen überstreicht.

    Johannes Kepler gelang es, diesen Zusammenhang zu entdecken, indem er Daten auswertete, die von Tycho Brahe gesammelt wurden. Er konnte dies berechnen, ohne die mathematische Lösung des Zweikörperproblems zu kennen. Eine vollständige Lösung erfordert jedoch weitere Integrationen unter Berücksichtigung der Energieerhaltung und weiterer Faktoren. 

    [data/cropped/298800.jpg]

    ## Kegelschnitte und die numerische Exzentrität

    Die erhaltenen Gleichungen beschreiben die Lösung für den Radiusvektor in Abhängigkeit vom Winkel, wobei es sich um einen Kegelschnitt handelt. Dabei sind P und E beides Konstanten, die vom jeweiligen System abhängen – beispielsweise Massen. Es ist nicht entscheidend, welche Größen genau in diesen Konstanten stecken, sondern lediglich, dass sie konstant sind. Die Konstante E wird dabei als numerische Exzentrizität bezeichnet und kann tatsächlich verändert werden.

    Betrachten wir eine kleine Ellipse mit einem Schwerpunkt oder Brennpunkt, dann stellt R den Radius dar, der von einem Startpunkt bei 0 über den Winkel Theta, der von 0 bis 360 Grad reicht, die Ellipse beschreibt. Wenn die numerische Exzentrizität gleich 1 ist, erhalten wir eine Ellipse. Die Konstante P ist jedoch fest und kann nicht verändert werden, während die numerische Exzentrizität durch die Geschwindigkeit beeinflusst werden kann.

    Stellen Sie sich vor, wir hätten die Erde oder einen anderen Planeten und bauen darauf einen sehr hohen Turm. Von diesem Turm werfen wir eine kleine Masse mit einer Geschwindigkeit V parallel zur Erdoberfläche weg. Abhängig von der Wurfstärke können unterschiedliche Ergebnisse erzielt werden. In den meisten Fällen kracht die Masse einfach auf den Boden. Dieser Fall entspricht einer Parabel.

    [data/cropped/438766.jpg]
    [data/cropped/438767.jpg]

    ## Flugbahnen und Fluchtgeschwindigkeit

    Betrachten wir nun den Fall 2. Hierbei wird mit sehr hoher Geschwindigkeit geworfen. Wichtig ist, dass der Turm, von dem aus geworfen wird, hoch genug sein muss, um atmosphärische Störungen auszuschließen. Bei ausreichender Wurfstärke entsteht ein Kreis. Der einzige Unterschied zu vorherigen Fällen ist die Geschwindigkeit. Erhöht man die Geschwindigkeit noch weiter, entsteht eine Ellipse, also Fall 3. Obwohl die Flugbahn komplexer wird, bleibt die Masse gebunden und kehrt, egal wie stark geworfen wird, zum Ausgangspunkt zurück. Allerdings ist die zurückgelegte Strecke deutlich größer als die Höhe des Turms.

    Mit Fall 4, bei noch höherer Geschwindigkeit, wird aus der Ellipse eine Hyperbel. Ab diesem Punkt verlässt die Masse den Einflussbereich des Planeten. Zusammenfassend lässt sich sagen, dass die Flugbahn – also ob Parabel, Kreis, Ellipse oder Hyperbel – allein durch die Wurfgeschwindigkeit bestimmt wird. 

    Nun stellt sich die Frage nach der konkreten Geschwindigkeit, die benötigt wird, um beispielsweise der Erde zu entfliehen, also die sogenannte Fluchtgeschwindigkeit. Um diese zu berechnen, müssen wir zunächst die Energie betrachten, die in der Bewegung um einen Schwerpunkt steckt.
    [data/cropped/527366.jpg]
    [data/cropped/527367.jpg]

    ## Energiebetrachtung bei Bahnbewegung

    Und wenn wir jetzt die Energie in diesem System berechnen, dann ist das relativ einfach. Wichtig ist, dass wir das nur für den kleinen Körper tun. Der große Körper könnte man das äquivalent machen, aber wir wollen es erstmal nur für den kleinen Körper machen. Die Gesamtenergie ist nichts anderes als die Summe der beiden Energien, die wir kennen: die kinetische Energie und die potentielle Energie. Beide sind bekannt: 1,5 mv² und -GmM/r. Achten Sie darauf, dass in der Kraft immer r², in der Energie aber nur r vorkommt. Da wir die Energieerhaltung kennen, können wir direkt sagen, dass das Ganze eine Konstante ist, solange in unserem System keine Energie nach außen abfließt, was wir ausschließen wollen. Daraus folgt direkt: Wenn die Bahn festgelegt ist, muss ein leichterer Körper schneller sein als ein schwererer Körper – das ist nicht verwunderlich und hätten wir auch mit dem Kraftansatz herausgefunden. Betrachten wir einen kompletten Umlauf, also alle Winkel von 0 bis 360 Grad, und bilden den Mittelwert, dann erhalten wir eine interessante Beziehung, den sogenannten Virialsatz. Der Mittelwert der kinetischen Energie ist betragsmäßig genau die Hälfte vom Mittelwert der potenziellen Energie. Die Herleitung dazu finden Sie in der klassischen Mechanik. Da dies ein wichtiger Satz ist, schreiben wir ihn nochmals auf: Das zeitliche Mittel der kinetischen Energie entspricht betragsmäßig dem zeitlichen Mittel der halben potenziellen Energie. Diese Beziehung nutzen wir nun, um die Bahngeschwindigkeit zu bestimmen. Dazu betrachten wir auf der Bahn zwei spezielle Punkte. Um die Geschwindigkeit zu bestimmen, müssen wir zuerst die quantitative Gesamtenergie bestimmen. Bisher wissen wir, dass es sich um eine Konstante handelt, aber nun wollen wir ihren Wert bestimmen. Dazu nutzen wir die Energie am sogenannten Perihälion, also dem Punkt, an dem sich der Schwerpunkt und der Körper am nächsten sind. 

    Um dies zu verdeutlichen, stellen wir uns vor, der Schwerpunkt befindet sich hier und die Masse hier. Ein halben Umlauf später befindet sich die Masse hier, und dieser Punkt ist das Perihälion. Als nächstes betrachten wir die Energie am Aphelion, dem Punkt, der am weitesten vom Schwerpunkt entfernt ist. Beachten Sie, dass die Linie, die die beiden Massen zu unterschiedlichen Zeitpunkten mit dem Schwerpunkt verbindet, immer zweimal die große Halbachse beträgt. Dies benötigen wir später noch. 

    Betrachten wir die Energie am Perihälion: Die Gesamtenergie E₀ ist 1/2 mvₚ² - GMm/rₚ. Multiplizieren wir diese Gleichung mit rₚ², erhalten wir E₀rₚ² = 1/2 mvₚ²rₚ² - GMm rₚ. Dies ist Gleichung 1. Auf der anderen Seite betrachten wir das gleiche am Aphelion: Die Energie ist wieder E₀, da die Gesamtenergie konstant bleibt. Die Gleichung lautet 1/2 mvₐ² - GMm/rₐ. Multiplizieren wir auch diese Gleichung mit rₚ², erhalten wir E₀rₚ² = 1/2 mvₐ²rₚ² - GMm rₚ. Dies ist Gleichung 2. 

    Nun folgt eine Zwischenfolgerung: Da der Drehimpuls erhalten bleibt, gilt vₐrₐ = vₚrₚ. Folglich ist 1/2 mvₚ²rₚ² = 1/2 mvₐ²rₐ². Subtrahieren wir Gleichung 2 von Gleichung 1, erhalten wir auf der linken Seite E₀rₚ² - E₀rₚ². Auf der rechten Seite kürzen sich die kinetischen Terme weg, da sie gleich sind. Es bleiben nur die Gravitationsterme übrig. Wir klammern -GMm aus und erhalten -GMm (1/rₐ - 1/rₚ). Vereinfachen wir dies weiter, erhalten wir -GMm (rₚ - rₐ) / (rₐrₚ). Wenn wir uns daran erinnern, dass die doppelte große Halbachse (2a) die Summe aus rₐ und rₚ ist, vereinfacht sich dies zu -GMm / 2a. Somit haben wir E₀ bestimmt. Die Gesamtenergie in diesem System für die eine Masse ist also -GMm / 2a.

    [data/cropped/1001733.jpg]

    ## Berechnung der Bahngeschwindigkeit und Fluchtgeschwindigkeit

    Um die Bahngeschwindigkeit zu berechnen, betrachten wir zunächst die Gesamtenergie des Systems, die wir bereits als 1,5mV² - GMm/R definiert haben. Diese Energie kennen wir nun genauer, da wir wissen, dass sie auch als -GMm/(2a) ausgedrückt werden kann. Durch Auflösen dieser Gleichung nach V erhalten wir die Bahngeschwindigkeit in Abhängigkeit des Radiusvektors: V = √(2GM(1/R - 1/(2a))). Der Rest der Größen ist konstant, sodass die Geschwindigkeit allein vom Radius abhängt.

    Betrachten wir nun das Problem, wie schnell ein Objekt geworfen werden muss, um dem Gravitationsfeld eines Körpers zu entkommen – also, um eine Hyperbelbahn zu erzeugen. Im Grenzübergang wird eine Hyperbel zu einer Ellipse mit unendlicher Halbachse. Wenn wir den Abstand 'a' gegen unendlich gehen lassen, nähert sich die Gesamtenergie Null, was bedeutet, dass das Teilchen ungebunden ist. Setzen wir diesen Wert in die Formel ein, erhalten wir die Fluchtgeschwindigkeit.

    Die Fluchtgeschwindigkeit ist also die Geschwindigkeit, die erforderlich ist, um eine Hyperbelbahn zu erreichen, und wird durch V_Flucht ≥ √(2GM/R) gegeben. Für die Erde beträgt diese Geschwindigkeit etwa 11,2 Kilometer pro Sekunde.
    """
    # keywords = create_keywords(script)
    # print(keywords)
    create_typst_document(aaa, key)