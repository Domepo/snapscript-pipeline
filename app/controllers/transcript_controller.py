import os
from models.transcript import get_transcript_by_id
from models.image_marker import get_image_markers_for_transcript

def reconstruct_transcript_with_images(transcript_id: int) -> str | None:
    full_text = get_transcript_by_id(transcript_id)
    if not full_text:
        return None

    markers = get_image_markers_for_transcript(transcript_id)
    markers.sort(key=lambda m: m['char_offset'], reverse=True)

    parts = []
    last_offset = len(full_text)

    for marker in markers:
        offset = marker['char_offset']
        placeholder = f"\n[BILD: {os.path.basename(marker['image_path'])}]\n"
        parts.append(full_text[offset:last_offset])
        parts.append(placeholder)
        last_offset = offset

    parts.append(full_text[:last_offset])
    return "".join(reversed(parts))
