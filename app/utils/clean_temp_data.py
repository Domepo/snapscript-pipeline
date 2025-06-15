import os

def clean_temp_data_files_only(directories):
    """
    Löscht nur Dateien in den angegebenen Verzeichnissen – keine Ordner selbst.
    
    :param directories: Liste von Ordnerpfaden, z. B. ["data/tmp", "data/cropped"]
    """
    for directory in directories:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                        print(f"🧹 Datei gelöscht: {file_path}")
                    elif os.path.isdir(file_path):
                        # Optional: leeren Unterordner löschen
                        try:
                            os.rmdir(file_path)
                            print(f"📁 Leerer Unterordner gelöscht: {file_path}")
                        except OSError:
                            # Ordner ist nicht leer
                            pass
                except Exception as e:
                    print(f"❌ Fehler beim Löschen von {file_path}: {e}")
        else:
            print(f"⚠️ Ordner nicht gefunden: {directory}")