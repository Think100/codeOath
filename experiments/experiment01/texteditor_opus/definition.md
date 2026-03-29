# texteditor_opus

## Was es ist

Ein minimaler Texteditor als **Architektur-Beispiel** fuer codeOath.
Zeigt Ports-and-Adapters an einem kleinen, vollstaendig funktionsfaehigen Programm.

**Features:**
- Textdateien oeffnen und bearbeiten
- Speichern (Ctrl+S) und Speichern unter
- Always-on-top Toggle
- Transparenz-Slider

## Was es NICHT ist

| Ausschluss | Grund |
|---|---|
| Kein produktiver Editor | Das ist ein Architektur-Beispiel, kein Ersatz fuer VS Code |
| Kein Syntax-Highlighting | Feature-Creep; nicht relevant fuer das Architektur-Muster |
| Keine Tabs / Multi-Document | Ein Dokument reicht um das Pattern zu zeigen |
| Kein Plugin-System | Overengineering fuer ein Beispiel |
| Keine Konfigurationsdatei | Haelt das Beispiel einfach und selbsterklaerend |

## Architektur

```
domain/          Reine Geschaeftslogik, keine Abhaengigkeiten
  model.py       Document, WindowState (Datenstrukturen + Regeln)
  ports.py       Protocols: FileReader, FileWriter, Incoming Ports

application/     Use Cases, Orchestrierung
  use_cases.py   OpenDocument, SaveDocument, SaveDocumentAs, UpdateContent

adapters/        Konkrete Implementierungen
  filesystem.py  LocalFileReader, LocalFileWriter (Outgoing Adapter)
  tkinter_ui.py  EditorWindow (Incoming Adapter)

main.py          Composition Root: verdrahtet alles
```

## Abhaengigkeitsrichtung

```
main.py  -->  adapters/  -->  application/  -->  domain/
                                  |                  ^
                                  +------------------+
```

Domain kennt nichts ausser sich selbst.
Application kennt Domain und Ports, aber keine konkreten Adapter.
Adapter kennen Ports und Domain-Typen.
Nur main.py kennt alle konkreten Typen.

## Ausfuehren

```
python main.py
```

Voraussetzung: Python 3.14+ mit tkinter (in Standard-Python enthalten).
