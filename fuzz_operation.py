from thefuzz import fuzz
from thefuzz import process

def split_transcript_into_paragraphs(transcript_text:str):
    """
    Teilt einen Transkripttext anhand von Zeilenumbrüchen in eine Liste von Absätzen auf.
    """

    paragraphs = [para.strip() for para in transcript_text.strip().split('\n') if para.strip()]
    return paragraphs


def find_paragraph_with_fuzzing(source:str, findable_string:str):
    best_match = process.extractOne(
        findable_string,
        split_transcript_into_paragraphs(source),
        scorer=fuzz.token_set_ratio
    )[0]
    return best_match