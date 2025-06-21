# Verwende ein schlankes Python-Image
FROM python:3.11-slim

# System-Dependencies für ffmpeg (Whisper/av), OpenCV etc.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      git \
      ffmpeg \
      libgl1 \
      libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*



# Arbeitsverzeichnis
WORKDIR /app

# Zuerst nur requirements kopieren, damit Docker Layer Caching greift
COPY requirements.txt .

# pip updaten und Python-Dependencies installieren
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# vor dem Kopieren deines Codes
RUN mkdir -p \
      data/videos \
      data/tmp \
      data/cropped \
      data/cropped_failed \
      data/transcript \
      data/pdf
# Restlichen Code kopieren
COPY . .

# Damit Streamlit nicht im Watch-Modus crasht
ENV STREAMLIT_WATCHER_TYPE=none

# Port freigeben (standardmäßig 8501)
EXPOSE 8501

# Default-Kommando: Starte Streamlit
CMD ["streamlit", "run", "app/main.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0"]
