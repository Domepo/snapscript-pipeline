from thefuzz import fuzz
from thefuzz import process
import fuzz_operation as fo
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
Was dann zu einer CCU geht, wo ich jetzt hin gehen will.'''


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