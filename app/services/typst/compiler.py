# compiler.py

import typst
from typing import Dict

def compile_document(sys_inputs: Dict,
                     typst_input: str,
                     pdf_output: str,
                     root_path: str) -> None:
    """
    Führt den Typst-Compiler mit den gegebenen System-Inputs aus.
    - sys_inputs: Dict mit JSON-Strings für "first_person", "heading" und "sections"
    - typst_input: Pfad zur .typ-Datei (z. B. new.typ)
    - pdf_output:   Pfad zur Ausgabedatei (z. B. ages.pdf)
    - root_path:    Wurzelverzeichnis, in dem sich Typst-Quellen und Bilder befinden
    """
    typst.compile(
        input=typst_input,
        output=pdf_output,
        root=root_path,
        sys_inputs=sys_inputs
    )
