# blog_sonnet_codeoath

Einfaches lokales Blog-System. Markdown-Dateien werden als HTML-Seiten gerendert.

## NOT
- Kein User-Login oder Authentifizierung
- Keine Datenbank (Dateisystem reicht)
- Kein Deployment (lokaler Dev-Server genuegt)
- Kein CMS-Editor (Markdown-Dateien werden manuell erstellt)
- Kein Kommentarsystem

## Rules
- Python 3.14+
- Code und Kommentare in Englisch
- Fehler werden dem User angezeigt, kein stilles Schlucken
- Neue Abhaengigkeiten: erst fragen
- Architektur proportional zur Problemgroesse

## Structure
- src/ -- application source
  - domain/ -- post model, port contracts
  - infrastructure/ -- file loading, markdown rendering
  - web/ -- Flask routes and templates
- posts/ -- Markdown post files
- tests/ -- unit tests
- docs/ -- ADRs and todo
