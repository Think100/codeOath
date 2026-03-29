# Architektur-Entscheidungen

## 1. Ports-and-Adapters-Struktur

**Kontext:** Das Projekt ist klein, aber soll die Trennung von Domain und Infrastruktur demonstrieren.

**Entscheidung:** Domain-Logik (Model, Service) kennt keine konkreten Implementierungen. Infrastruktur (Dateisystem, Markdown-Lib, Flask) implementiert die in `ports.py` definierten Protocols.

**Konsequenz:** Domain-Tests brauchen weder Flask noch Dateisystem. Adapter sind austauschbar.

## 2. Front-Matter statt Datenbank

**Kontext:** Posts sollen als Markdown-Dateien geschrieben werden.

**Entscheidung:** Metadaten (Titel, Datum, Tags) werden als YAML-aehnlicher Front-Matter-Block am Anfang jeder .md-Datei gespeichert. Kein externer YAML-Parser, nur einfaches String-Parsing.

**Konsequenz:** Keine Datenbank noetig. Posts sind versionierbar mit Git. Einschraenkung: kein verschachteltes YAML.

## 3. Flask als Web-Framework

**Kontext:** Es wird ein leichtgewichtiges Python-Web-Framework benoetigt.

**Entscheidung:** Flask, weil es minimal ist und zum Problemumfang passt.

**Konsequenz:** Einfaches Setup, geringe Abhaengigkeiten.
