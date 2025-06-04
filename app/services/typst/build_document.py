
from builders import (
    build_first_person,
    build_heading,
    build_section,
    build_sys_inputs
)


from compiler import compile_document


if __name__ == "__main__":
    # === 1. Metadaten definieren ===
    first_person = build_first_person(
        name="Prof. Dr. rer. nat. Vorname Nachname",
        uni="Beispiel-Universität",
        email="email@beispiel.de",
        phone="+49 1234 567890"
    )

    heading = build_heading(
        title="Dein Kurstitel",
        abstract=(
            "Hier kommt die Zusammenfassung deiner Vorlesung/dokument. "
            "Beschreibe knapp, worum es geht."
        ),
        keywords=["Stichwort1", "Stichwort2", "Stichwort3"],
        date="4 Juni, 2025"
    )

    # === 2. Abschnitte (Sections) definieren ===
    sections = []

    # Beispielabschnitt "Einführung"
    intro_content = [
        {
            "type": "text",
            "value": "Einleitender Text hier einfügen. Beschreibt den Zweck des Dokuments."
        },
        {
            "type": "image",
            "path": "/cropped/crop_0_camera-3.jpg",
            "caption": "Beispielbild für die Einführung",
            "width": 0.5
        },
        {
            "type": "text",
            "value": "Weiterer Begleittext oder eine zweite Textzeile."
        }
    ]
    sections.append(build_section(name="Einführung", content=intro_content))

    # Beispielabschnitt "Methodik"
    methodology_content = [
        {
            "type": "text",
            "value": "Beschreibung der Methodik: Wie wurden Daten erhoben?"
        },
        {
            "type": "image",
            "path": "/cropped/crop_0_camera-3.jpg",
            "caption": "Methodisches Schema",
            "width": 0.5
        }
    ]
    sections.append(build_section(name="Methodik", content=methodology_content))

    # Weitere Abschnitte analog:
    # sections.append(build_section(name="Ergebnisse", content=[ ... ]))
    # sections.append(build_section(name="Fazit", content=[ ... ]))

    # === 3. Sys-Inputs zusammenbauen ===
    sys_inputs = build_sys_inputs(
        first_person=first_person,
        heading=heading,
        sections=sections
    )

    # === 4. Dokument kompilieren ===
    typst_input_path = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data/typst/lecture.typ"
    pdf_output_path   = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data/typst/lecture.pdf"
    root_directory    = "C:/Users/domin/Documents/02_Github/snapscript-pipeline/data"

    compile_document(
        sys_inputs=sys_inputs,
        typst_input=typst_input_path,
        pdf_output=pdf_output_path,
        root_path=root_directory
    )

    print("Kompilierung abgeschlossen!")
