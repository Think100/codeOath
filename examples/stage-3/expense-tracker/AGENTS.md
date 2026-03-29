# expense-tracker

CLI tool to track personal expenses from the terminal.

---

## NOT

Dieses Projekt ist bewusst begrenzt. Folgendes gehoert nicht zum Scope:

| Was                              | Warum nicht                                                    |
| -------------------------------- | -------------------------------------------------------------- |
| Kein Web-App                     | Einzel-User-Tool, kein Server noetig, kein Browser-Overhead.  |
| Kein Multi-Waehrungs-Tool        | Eine Waehrung reicht. Mehrwaehrungs-Support waere Scope Creep. |
| Kein Budgetierungs-/Forecast-Tool | Nur Erfassung, keine Planung. Andere Problem-Domaine.          |

---

## Rules

### Allgemein
- Python 3.14+
- Code (Variablen, Funktionen, Klassen) und Code-Kommentare: **Englisch**
- AGENTS.md und alle Dateien unter `docs/`: **Deutsch**
- Keine Secrets, Keys oder Credentials im Code oder in Commits

### Sprach-Konventionen

| Was                              | Sprache     | Warum                                      |
| -------------------------------- | ----------- | ------------------------------------------ |
| Code (Variablen, Klassen, Funkt.)| Englisch    | Universal, Libraries erwarten es           |
| Code-Kommentare                  | Englisch    | Gleiche Sprache wie der Code               |
| Commit-Messages (nach Praefix)   | Englisch    | Git-History durchsuchbar und konsistent    |
| AGENTS.md, CLAUDE.md             | Deutsch     | Dein Denk-Tool, deine Sprache              |
| docs/ (ADRs, TODOs, Definitionen)| Deutsch     | Interne Docs, Scope-Denken                 |
| README.md                        | Englisch    | Open-Source-Projekt, externe Leser         |
| AI-Antworten                     | Sprache des Users | Dynamisch, nicht fix                 |

### AI-spezifische Regeln
- Neue Dateien: erst fragen, nicht einfach anlegen
- Commit-Messages mit Praefix: `[claude]`, `[cursor]`, `[codex]` je nach Tool
- Niemals Commits amenden oder force-pushen ohne explizite Freigabe
- Niemals Dateien loeschen ohne Bestaetigung
- Im Zweifel: fragen statt raten

---

## Architecture

```
domain/       core logic, no external imports
application/  use cases, orchestration
adapters/     inbound (CLI), outbound (SQLite)
main          connects everything

Rule: domain imports nobody. application imports domain. adapters import both.

Enforcement: import-linter (pyproject.toml), pre-commit hook, CI.
For detailed layer rules: see .claude/rules/
```

---

## Structure

```
src/expense_tracker/   Quellcode (installierbar via pip install -e .)
  domain/              Reine Logik, keine externen Imports
  application/         Use Cases, Orchestrierung
  adapters/
    inbound/           CLI (Click)
    outbound/          SQLite-Repository
tests/                 Pytest-Tests (domain, application, adapters getrennt)
docs/                  Interne Dokumentation auf Deutsch
  adr/                 Architecture Decision Records
config/                Einstellungen (DEFAULT_DB_PATH etc.)
```

---

## Navigation

```
For business logic:           src/expense_tracker/domain/
For CLI changes:              src/expense_tracker/adapters/inbound/cli.py
For database:                 src/expense_tracker/adapters/outbound/sqlite_repo.py
For use cases:                src/expense_tracker/application/use_cases.py
For architecture decisions:   docs/adr/
```
