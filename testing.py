from thefuzz import fuzz
from thefuzz import process
import app.services.fuzzing_service as fo
FULL_TRANSRIPT_TEXT = '''Ja, herzlich willkommen zur heutigen Vorlesung. Heute soll es um Livestream-Technik gehen.
Genau, da unterteilen wir verschiedene Bereiche. Also wir haben einen Bildbereich,
einen Videobereich, natürlich die Lichtbereiche, sozusagen wie das alles ausgeleuchtet werden
muss. Und das werden wir in so einem schönen Diagramm haben. Nämlich das sind die verschiedenen
Ebenen. Denn wir haben natürlich ganz oben das, was man sieht. Also das, was man sieht,
ist ein Auge. Dann haben wir hier natürlich die Kabel und die ganzen Verbindungen. Und
unten haben wir dann Software. Genau. Wichtig ist auch, das ist ein Zitat von mir. Das OBS ist
das Tor zum guten Livestream. Ja, dann würde ich einmal gerne mit den Kameras anfangen. Genau, hier symbolisch
eine Kamera. Also wir haben natürlich verschiedene Möglichkeiten. Es gibt natürlich HDMI-betriebene
Kameras. HDMI. Wir haben auch SDI-Kameras. Und wir haben natürlich auch Glasfaser und auch noch IP, also
Ethernet Kameras. Bei HDMI ist es so, dass wir nur kurze Strecken, kurze Strecken, aber hohe Bandbreite.
Bei SDI haben wir sehr lange Strecken und, ja, eine etwas niedrigere Bandbreite. Glasfaser haben wir dann gigantische
Strecken, gigantische Bandbreite. Und bei IP Ethernet haben wir, ist ja das Ding, dass man vielleicht noch mit ein paar
Latenzen zu kämpfen hat. Aber seit dem neuen IP2110-Standard von MacMagic ist das auch schon, ja, nicht mehr so wichtig.
Genau, wie ist eine Kamera aufgebaut? Wir haben zum einen, das nennt man Buddy. Dieses Buddy
ist dann das Kamera mit einem gewissen Bayonet. Und das ist hier das Bayonet. Und da gibt es verschiedene Optionen.
Man hat, ähm, man hat, ähm, man hat EF, ähm, Bayonet zum Beispiel von Canon. Also, hier kann ich einfach hinschreiben.
Canon ist gleich EF. Fujifilm hat mehrere. Eins davon ist die XF-Serie. Aber das ist einfach nur der Verschluss für das Objektiv,
was dann hierhin kommt. Hier ist das Objektiv. Und an dem Objektiv kann man auch noch Filter dran machen.
Filter. Und da gibt es zum Beispiel UV-Filter. Also es gibt verschiedenste Filter. UV, wir haben NDE, wir haben Mistfilter für so einen Glow-Effekt.
Und, ja, dann haben wir auch noch, gibt es auch noch, ähm, ähm, Variable, Variable ND. Da komme ich aber später nochmal zu.
Ein Buddy hat auch noch die Möglichkeit, dass man hier Anschlüsse hat. Zum Beispiel ein In-STI und ein Out-STI.
Was dann zu einer CCU geht, wo ich jetzt hin gehen will.
Und zwar, ähm, haben wir jetzt CCU.
Was ist CCU? Camera Control Unit. Genau. Also, das ist, ähm, Camera.
Damit lassen sich dann da Kameras steuern. Das ist von Blackmagic zum Beispiel so ein Teil hier.
Hier hat man dann verschiedene Knöpfe.
Dann hat man meistens noch so einen großen Regler, mit dem man hoch- und runterschieben kann.
Natürlich hier noch die Program-Knöpfe und Preview-Knöpfe.
Und dann hat man auch noch, ja, verschiedene Texte. Hier gibt es so Labels.
Jetzt steht hier Text, Text, Text. So.
Und damit ist es dann möglich. Zum einen den Fokus. Zum einen den Zoom.
Und dann noch verschiedene Bildwerte wie Weißabgleich, den Iris, also die Verblende.
Dann auch noch Farbkorrekturen. Also können wir LUTZ nennen.
Lookup Tables. Und die gehen dann gebündelt durch ein Kabel.
Das ist das SDI-Out. Weil das ja... Ne, das ist... Also von dieser Perspektive ist das SDI-Out.
Und das geht dann... Hier haben wir ja die Kamera. Das geht dann in den SDI-In.
Und der SDI-Out von der Kamera, der geht dann in einen Recorder rein.
Zum Beispiel in einen PC. Und der schmeißt das dann in OBS.
Genau. Was ist OBS? Kommen wir jetzt zu.
OBS ist der Open Broadcaster Software.
Und da haben wir zum einen, ja, den PC mit einem Record, mit einer Recording-Card.
Zum Beispiel auch von Blackmagic. Blackmagic, 4K-Karte. Ist auch eigentlich egal.
Und da gehen dann die Signale von der CCU... Äh, von dem SDI-Out rein.
Der dann ja auch wieder von einem Videomischer kommt. Komme ich nachher zu.
Und OBS nimmt jetzt dieses Signal. Also das ist jetzt sozusagen im PC drin.
PC in Verbindung. Und dann hat OBS eine schöne Oberfläche.
Hier hat man die Quellen. Dann hat man hier zum Beispiel Einstellungen.
Und hier hat man dann Stream starten und alles mögliche.
Hier kann man das dann so einstellen, dass man zum einen ein Program und ein Preview hat.
Also einmal ein Program und ein Preview.
Oder andersrum. Kann man noch tauschen, wie man lustig ist.
Und dadurch kann dieses Signal dann zu YouTube geschickt werden.
Ja. Dann gucken wir uns mal an, was passiert, was ist bei YouTube.
Also bei YouTube haben wir die Möglichkeit, diesen Stream bereit zu stellen.
Ähm, gleichzeitig haben wir auch noch die Möglichkeit, ja, Analytics.
Analytics. Also, ne, wie die Zuschauerzahlen aussehen.
Dann haben wir auch noch Moderationsfunktionen.
Moderationsfunktionen. Darunter zählen dann Kommentare, Likes etc.
Ja. Und das alles ist dann recht wichtig, damit man einen Überblick hat, wie ein Stream ankommt.
Genau. Und ich habe davor über einen Videomischer geredet.
Einen Videomischer. Weil wir haben ja jetzt zum Beispiel, also den brauchen wir.
Oder sagen wir mal so, der Sollzustand ist mehrere Kameras und Steuerung aller Kameras.
Also machen wir Kamera mal n ist gleich f von x hoch n minus die Wurzel aus YouTube.
Genau. Recht einfache Gleichung.
Ähm, aus der folgt dann natürlich auch, dass e gleich m c Quadrat ist.
Ne, ganz simpel, wegen dem n, was hier sich ja zum e transformiert.
Und dadurch hat man ja dann auch die Fourier transformierte der inneren Steigungsfunktion vom Tangentenbeispiel.
Wie bereits gesagt, also das Integral von d von x minus, ja, 100 f z hoch Pi cos sin von x.
Klammer zu.
Genau. Und das, der Videomischer sieht dann wie folgt aus.
Man hat hier die Knöpfe.
Hier oben hat man Knöpfe.
Und dann hat man hier einen Regler, den man hoch oder runter schieben kann.
Und an dieses Gerät kann man dann Kameras anschließen, die dann auch mit der CCU verbunden werden.
Da haben wir zum Beispiel mal zwei Kameras.
Genau.
Und dann braucht das natürlich noch Strom, ne.
AC-Strom, meistens redundant.
Und das Ding ist zum Beispiel von Atem, von Blackmagic, ein Gerät.
Ja, so könnte ein Videomischer aussehen.
Warum machen wir das alles?
Wir wollen natürlich Zuschauerzeit und wir wollen auch gleichzeitig, dass sich die Bindung erhöht.
Also das heißt, dass sich die Zeit, wie lange ein Zuschauer drauf bleibt, auch erhöht in Bezug auf die Watchtime.
Ja, vielen Dank. Das war's auch schon.
'''


# Beispiel: in Zeilen aufteilen
lines = FULL_TRANSRIPT_TEXT.splitlines()

# oder in Sätze aufteilen (wenn jeder Satz mit Punkt endet)
# lines = FULL_TRANSRIPT_TEXT.split('.')

query = "Und hier das und da gibt es verschiedene Optionen."

# besten Treffer holen
best_match = process.extractOne(
    query,
    lines,
    scorer=fuzz.token_set_ratio  # oder fuzz.token_sort_ratio, je nach Bedarf
)

print(best_match)
# best_match ist ein Tuple: (matched_line, score, index)

# start_index = FULL_TRANSRIPT_TEXT.index("dass man hier Anschlüsse hat. Zum Beispiel ein In-STI") # Nutzt str.index, wirft ValueError wenn nicht gefunden
# print(start_index + len("dass man hier Anschlüsse hat. Zum Beispiel ein In-STI"))
relevant_section = "dass man hier Anschlüsse hat. Zum Beispiel ein In-STI"
relevant_section = fo.find_paragraph_with_fuzzing(FULL_TRANSRIPT_TEXT,relevant_section)
print(relevant_section)