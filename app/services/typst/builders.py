# builders.py

import json
from typing import List, Dict
import logging

def build_first_person(name: str, uni: str, email: str, phone: str) -> Dict:
    """
    Erzeugt die Metadaten zur ersten Person.
    """
    return {
        "name": name,
        "uni": uni,
        "email": email,
        "phone": phone
    }

def build_heading(title: str, abstract: str, keywords: List[str], date: str) -> Dict:
    """
    Erzeugt das Heading mit Titel, Abstract, Keywords und Datum.
    """
    return {
        "title": title,
        "abstract": abstract,
        "keywords": keywords,
        "date": date
    }

def build_section(name: str, content: List[Dict]) -> Dict:
    """
    Erzeugt einen Abschnitt mit Name und einer Liste von Content-Elementen.
    Content-Elemente sind Dicts mit "type" ("text" oder "image") und den Feldern:
      - Text:   {"type": "text",  "value": "..."}
      - Image:  {"type": "image", "path": "...", "caption": "...", "width": 0.5}
    """
    return {
        "name": name,
        "content": content
    }

def build_sys_inputs(first_person: Dict, heading: Dict, sections: List[Dict]) -> Dict:
    """
    Wandelt die Daten in JSON-Strings um, wie es Typst erwartet.
    """
    return {
        "first_person": json.dumps(first_person),
        "heading":      json.dumps(heading),
        "sections":     json.dumps(sections)
    }
