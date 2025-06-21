# 🎬 Video2Script‑Pipeline

![Alt Text](assets\output.gif)
*Vom Vorlesungs‑Video zum strukturierten Skript & PDF – vollautomatisch.*
## Über das Projekt

Video2Script verwandelt aufgezeichnete Vorlesungen (oder andere Bildschirm‑/Kamera‑Videos) in ein sauber gegliedertes Skript inkl. Bildern, Schlagwörtern und fertigem PDF‑Export.
Dazu kombiniert der Workflow mehrere KI‑Modelle und Open‑Source‑Tools:

1. **Whisper** transkribiert den Ton des Videos.
2. **YOLO‑v11** erkennt Folien‑ und Tafel‑Abschnitte im Video‑Stream.
3. **Ollama + Gemma 3:27b ⚙︎** analysiert Bilder & Text, erzeugt Keywords und poliert das Skript.
4. **Typst** rendert das Markdown‑Skript zu einem hübschen PDF.
5. **Streamlit** bildet die interaktive Benutzeroberfläche.

Das Ergebnis ist ein lesefertiges Skript (Markdown + PDF), das Lehrende direkt an Studierende verteilen können.

---

## Table of Contents

* [Über das Projekt](#über-das-projekt)
* [Verwendete Libraries](#verwendete-libraries)
* [Beispiel‑Output](#beispiel-output)
* [Installation](#installation)

  * [Docker‑Quickstart](#docker-quickstart)
  * [Lokale Python‑Umgebung](#lokale-python-umgebung)
* [Ausführung](#ausführung)
* [Dokumentation](#dokumentation)

---

## Verwendete Libraries

| Kategorie                         | Wichtigste Pakete                                  |
| --------------------------------- | -------------------------------------------------- |
| **Speech‑to‑Text**                | `openai-whisper`                                   |
| **Bild‑/Objekterkennung**         | `ultralytics` (YOLO v8)                            |
| **Large‑Language‑Model**          | `ollama`, `gemma3:27b`                             |
| **Dokument‑Rendering**            | `typst`                                            |
| **UI / Server**                   | `streamlit`, `fastapi`                             |
| **Computer Vision & Bildanalyse** | `opencv-python`, `scikit-image`, `imagehash`       |
| **Data & Utilities**              | `pandas`, `numpy`, `tqdm`, `psutil`, `coloredlogs` |

*Die vollständige Liste aller Python‑Abhängigkeiten findest du in [`requirements.txt`](requirements.txt).*

---

## Beispiel‑Output

```text
/data/pdf/astro_vorlesung.pdf
```

<p align="center">
  <img src="assets\example.png">
</p>

---

## Installation
Wir empfehlen die Nutzung von Docker
### Docker‑Quickstart

```bash
# Ollama – benötigt das Gemma‑3‑Modell (≈ 19 GB)
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama ollama/ollama
# optional: Modell vorab laden
docker exec -it ollama ollama run gemma3:27b

# Video2Script‑Container bauen & starten
docker build -t video2script .
docker run -d --name video2script \
  --link ollama:ollama \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data video2script
```
Der Container ist nun über `localhost:8501` errecihbar
### Lokale Python‑Umgebung

```bash
python -m venv venv
source venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# ffmpeg & system libs werden unter Linux via apt installiert (siehe Dockerfile)
```

---

## Ausführung

1. **Streamlit‑App starten** (nur nötig außerhalb des Docker‑Containers):

   ```bash
   streamlit run app/main.py
   ```
2. Im Browser `http://localhost:8501` öffnen.
3. Video (MP4) hochladen und den Fortschrittsbalken abwarten.
4. PDF herunterladen oder Skript‑/Keyword‑Vorschau anzeigen.

---

## Dokumentation

* Technischer Ablauf & Code‑Dokumentation findest du in den Docstrings der Module unter `app/*`.
* **Datenbank‑Schema** wird beim ersten Lauf automatisch unter `presentation_slides.db` erzeugt (SQLite).
* Für tiefergehende Infos lies die Kommentare im [Dockerfile](dockerfile) und im Source‑Code.

> **Tipp:** Aktiviere `logging` auf Level `DEBUG`, um detaillierte Ausgaben über die Bild‑/Text‑Verknüpfung zu erhalten.

---

© 2025 – MIT Licence
