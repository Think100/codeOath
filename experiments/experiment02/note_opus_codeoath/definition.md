# note_opus_codeoath

## Was es ist

Eine minimale Desktop-Notiz-App als **Architektur-Beispiel** fuer codeOath.
Zeigt Ports-and-Adapters an einem kleinen, vollstaendig funktionsfaehigen Programm.

**Features:**
- Schnell Gedanken festhalten
- Automatisches Speichern (kein manuelles Save noetig)
- Always-on-top Toggle
- Transparenz-Slider
- Notizen bleiben nach Neustart erhalten

## Was es NICHT ist

| Ausschluss | Grund |
|---|---|
| Kein Multi-Note-System | Eine Notiz reicht um das Pattern zu zeigen |
| Kein Rich-Text / Markdown | Plain-Text haelt es einfach |
| Keine Cloud-Sync | Lokale Persistenz genuegt fuer das Beispiel |
| Keine Kategorien / Tags | Feature-Creep; nicht relevant fuer das Architektur-Muster |
| Keine Konfigurationsdatei | Haelt das Beispiel einfach und selbsterklaerend |

## Architektur

```
domain/          Reine Geschaeftslogik, keine Abhaengigkeiten
  model.py       Note, WindowState (Datenstrukturen + Regeln)
  ports.py       Protocols: NoteStorage, Incoming Ports

application/     Use Cases, Orchestrierung
  use_cases.py   UpdateNote, LoadNote, SaveNote

adapters/        Konkrete Implementierungen
  json_storage.py  JsonNoteStorage (Outgoing Adapter)
  tkinter_ui.py    NoteWindow (Incoming Adapter)

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
