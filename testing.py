from thefuzz import fuzz
from thefuzz import process
full_transcript_list = [
    "Ja, herzlich willkommen zur heutigen Vorlesung. Heute soll es um Livestream-Technik gehen.",
    "Genau, da unterteilen wir verschiedene Bereiche. Also wir haben einen Bildbereich, einen Videobereich, natürlich die Lichtbereiche, sozusagen wie das alles ausgeleuchtet werden muss.",
    "Und das werden wir in so einem schönen Diagramm haben. Nämlich das sind die verschiedenen Ebenen.",
    "Denn wir haben natürlich ganz oben das, was man sieht. Also das, was man sieht, ist ein Auge.",
    "Dann haben wir hier natürlich die Kabel und die ganzen Verbindungen.",
    "Und unten haben wir dann Software.",
    "Genau. Wichtig ist auch, das ist ein Zitat von mir. Das OBS ist das Tor zum guten Livestream.",
    "Ja, dann würde ich einmal gerne mit den Kameras anfangen. Genau, hier symbolisch eine Kamera.",
    "Also wir haben natürlich verschiedene Möglichkeiten. Es gibt natürlich HDMI-betriebene Kameras. HDMI.",
    "Wir haben auch SDI-Kameras.",
    "Und wir haben natürlich auch Glasfaser und auch noch IP, also Ethernet Kameras.",
    "Bei HDMI ist es so, dass wir nur kurze Strecken, kurze Strecken, aber hohe Bandbreite.",
    "Bei SDI haben wir sehr lange Strecken und, ja, eine etwas niedrigere Bandbreite.",
    "Glasfaser haben wir dann gigantische Strecken, gigantische Bandbreite.",
    "Und bei IP Ethernet haben wir, ist ja das Ding, dass man vielleicht noch mit ein paar Latenzen zu kämpfen hat.",
    "Aber seit dem neuen IP2110-Standard von MacMagic ist das auch schon, ja, nicht mehr so wichtig.",
    "Genau, wie ist eine Kamera aufgebaut? Wir haben zum einen, das nennt man Buddy.",
    "Dieses Buddy ist dann das Kamera mit einem gewissen Bayonet.",
    "Und das ist hier das Bayonet. Und da gibt es verschiedene Optionen."
]

a=process.extract("Und  hier das Bayonet nd da gibt es verschiedene Optionen.", full_transcript_list, limit=1)

print(a[0][0])