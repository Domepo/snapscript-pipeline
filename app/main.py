import streamlit as st
import os
import config
from services.yolo_service import get_crop_image
from services.transcript_to_script_service import transcript_to_script_iterative
from services.typst.build_document import create_typst_document
from services.ollama_create_keywords import create_keywords
from controllers.transcript_controller import compare_image_text_timestamp
from controllers.video_whisper import generate_transcript, store_transcript
from models.database import init_db
from utils.token_count import count_tokens
from utils.video_to_image_timestamp import extract_frames_rename_by_timestamp
from utils.clean_temp_data import clean_temp_data_files_only
import torch
torch.classes.__path__ = []

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"


st.set_page_config(page_title="Video2Script", layout="wide")
st.title("🎬 Video zu Skript Generator")

if "step" not in st.session_state:
    st.session_state.step = 0

uploaded_file = st.file_uploader("📤 Lade dein Video hoch", type=["mp4"])

if uploaded_file:
    video_path = f"data/videos/{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Initialisiere Datenbank..."):
        init_db()

    st.session_state.step = 1

if st.session_state.step >= 1:
    with st.spinner("🔊 Generiere Transkript..."):
        # script = generate_transcript(video_path)
        # transcript_id = store_transcript(script, config.TRANSCRIPT_PATH)
        transcript_id = 11
        st.session_state.transcript_id = transcript_id
    st.success("✅ Transkript erstellt.")
    st.session_state.step = 2

if st.session_state.step >= 2:
    with st.spinner("🖼️ Extrahiere Frames..."):
        extract_frames_rename_by_timestamp(video_path, "data/tmp")
    st.success("✅ Frames extrahiert.")
    st.session_state.step = 3

if st.session_state.step >= 3:
    with st.spinner("📐 Bildausschnitte mit YOLO..."):
        get_crop_image("data/tmp", "data/cropped", "data/cropped_failed")
    st.success("✅ Bilder erkannt und ausgeschnitten.")
    st.session_state.step = 4

if st.session_state.step >= 4:
    with st.spinner("🔗 Verknüpfe Text & Bilder..."):
        script_with_images = compare_image_text_timestamp("data/cropped", st.session_state.transcript_id, "data/transcript/transcript_with_images.txt")
        config.OLLAMA_NUM_CTX = count_tokens(script_with_images)
    st.success("✅ Verknüpfung abgeschlossen.")
    st.session_state.step = 5

if st.session_state.step >= 5:
    with st.spinner("📝 Erzeuge finalen Skriptentwurf..."):
        final_script = transcript_to_script_iterative(script_with_images)
        st.session_state.final_script = final_script
    st.success("✅ Skript erzeugt.")
    st.session_state.step = 6

if st.session_state.step >= 6:
    with st.spinner("🔑 Extrahiere Keywords..."):
        keywords = create_keywords(st.session_state.final_script)
        st.session_state.keywords = keywords
    st.success("✅ Keywords erstellt.")
    st.session_state.step = 7

if st.session_state.step >= 7:
    with st.spinner("📄 Erstelle PDF mit Typst..."):
        video_filename = os.path.basename(video_path)
        pdf_name = os.path.splitext(video_filename)[0]  # z. B. "Astro"
        create_typst_document(st.session_state.final_script, st.session_state.keywords, pdf_name)

    st.success("✅ PDF generiert.")

    # Lokaler Pfad zum erzeugten PDF
    pdf_path = f"data/pdf/{pdf_name}.pdf"
    st.session_state.output_path = pdf_path

    if os.path.exists(pdf_path):
        # Download-Button
        with open(pdf_path, "rb") as f:
            st.download_button("📥 PDF herunterladen", f, file_name=f"{pdf_name}.pdf")

    # Text-Vorschau
    with st.expander("📃 Vorschau Skript"):
        st.text_area("Skript", st.session_state.final_script, height=300)

    with st.expander("🔑 Vorschau Keywords"):
        st.write(st.session_state.keywords)

with st.sidebar:
    if st.button("🔄 Neustart"):
        st.session_state.clear()
        st.experimental_rerun()

temp_dirs = [
    "data/cropped",
    "data/cropped_failed",
    "data/tmp",
    "data/videos"
]

clean_temp_data_files_only(temp_dirs)