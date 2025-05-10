# Koch LV Verarbeitung

Ein internes Tool für die Verarbeitung von Leistungsverzeichnissen (LV) im PDF-Format für die Firma Koch.

## Features

- PDF-Upload und Verarbeitung
- Bearbeitbare Datentabelle
- XML-Generierung und Export
- Live-Vorschau der Daten
- Kunden-ID Integration

## Installation

1. Erstellen Sie eine virtuelle Umgebung:
```bash
python -m venv venv
source venv/bin/activate  # Für Unix/MacOS
# oder
.\venv\Scripts\activate  # Für Windows
```

2. Installieren Sie die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Verwendung

1. Starten Sie die Anwendung:
```bash
streamlit run app.py
```

2. Öffnen Sie die Anwendung in Ihrem Browser (normalerweise unter http://localhost:8501)

3. Geben Sie eine Kunden-ID ein und laden Sie eine PDF-Datei hoch

4. Bearbeiten Sie die Daten in der Tabelle

5. Generieren und exportieren Sie das XML

## API Integration

Die Anwendung ist für die Integration mit einem Backend-Service vorbereitet. Aktuell werden die API-Aufrufe simuliert. Um die tatsächliche API-Integration zu aktivieren, bearbeiten Sie die `process_pdf`-Funktion in `app.py`.
