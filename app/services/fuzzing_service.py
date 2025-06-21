from thefuzz import fuzz, process

def split_paragraphs(text: str):
    return [p.strip() for p in text.strip().split('\n') if p.strip()]

def find_paragraph_with_fuzzing(source: str, query: str):
    paragraphs = split_paragraphs(source)
    result = process.extractOne(query, paragraphs, scorer=fuzz.token_set_ratio)
    return result[0] if result else None
