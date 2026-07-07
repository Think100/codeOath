# blog_fable_codeoath

Lokales Blog-System. Markdown-Dateien aus posts/ werden als HTML-Seiten
ausgeliefert: eine Uebersichtsseite (neueste zuerst) und eine Seite pro Post.

## NOT
- Kein Login, keine Benutzerverwaltung (laeuft nur lokal fuer eine Person)
- Keine Datenbank (Markdown-Dateien im Dateisystem reichen)
- Kein Web-Editor oder Admin-Bereich (Posts werden im Texteditor geschrieben)
- Kein Kommentarsystem, kein RSS (nicht angefragt)
- Kein Deployment-Setup (Flask-Dev-Server genuegt lokal)

## Rules
- Python 3.10+
- Code und Kommentare in Englisch
- Fehler sichtbar machen, nie still schlucken: kaputte Posts werden
  uebersprungen und auf der Startseite als Warnung gelistet
- posts/ ist Nutzerdaten: nie automatisch loeschen oder ueberschreiben
- Keine Secrets im Code oder in Git
- Neue Abhaengigkeiten: erst fragen, Grund nennen (AI rule)
- Neue Dateien: erst fragen (AI rule)
- Commits mit Tool-Prefix: [claude], [cursor], [codex] (AI rule)
- Bei Unsicherheit: fragen, nicht raten (AI rule)

## Structure
- Source: src/
  - src/domain/ -- Post-Modell, Sortierung, Tag-Filter, Port-Contract
  - src/adapters/ -- Dateisystem-Repository, Markdown-Rendering, Flask-Routen,
    Templates
  - Regel: domain/ importiert nie aus adapters/
- Entry point: app.py (Composition Root, verdrahtet Repository und Web-App)
- Posts: posts/ (eine .md-Datei pro Post, YAML-Frontmatter mit title, date,
  optional tags)
- Tests: tests/
- Docs: docs/
- Tasks und offene Fragen: docs/todo.md
