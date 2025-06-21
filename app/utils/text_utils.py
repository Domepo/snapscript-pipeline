import logging
def find_section_end_offset(full_text: str, section_to_find: str) -> int | None:
    """
    Findet den End-Offset (Position nach dem letzten Zeichen) des section_to_find im full_text.
    Gibt None zurück, wenn der Abschnitt nicht gefunden wird.
    """
    try:
        start_index = full_text.index(section_to_find)
        return start_index + len(section_to_find)
    except ValueError:
        logging.info(f"WARNUNG: Abschnitt nicht im Transkript gefunden:\n{section_to_find[:80]}...")
        return None
