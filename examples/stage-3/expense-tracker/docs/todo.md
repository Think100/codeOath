# Todo: expense-tracker

## Tasks

- [ ] CSV-Export hinzufuegen (`expense export --format csv`)
- [ ] Interaktiver TUI-Modus (Stretch Goal, z.B. mit `textual`)
- [ ] Kategorien-Validierung: pruefen ob vordefinierte Liste sinnvoll waere
- [ ] Paginierung fuer `expense list` bei vielen Eintraegen
- [ ] Shell-Completion (Click unterstuetzt das nativ, nur noch aktivieren)

## Routines

| Aufgabe                        | Frequenz    | Letztes Mal  |
| ------------------------------ | ----------- | ------------ |
| Abhaengigkeiten pruefen (pip)  | monatlich   | 2026-03-29   |
| Tests lokal ausfuehren         | bei Aenderung | 2026-03-29 |
| ADRs auf Aktualitaet pruefen   | quartalweise | 2026-03-29  |

## Open Questions

- Sollen Kategorien frei eingebbar sein (aktuell) oder aus einer vordefinierten Liste stammen?
  Freeform ist flexibler, aber fuehrt zu Tippfehlern (`food` vs. `Food` vs. `Essen`).
- Soll die DB-Datei per Konfigurationsdatei (`~/.config/expense-tracker/config.toml`) einstellbar
  sein, statt nur per Umgebungsvariable?
- Multi-Waehrung: explizit ausgeschlossen (siehe AGENTS.md NOT-Sektion), aber Waehrungs-Symbol
  fuer Ausgabe konfigurierbar machen?

## Resolved

- **SQLite vs. Flat File:** SQLite gewaehlt. Begruendung: siehe `docs/adr/0002-sqlite-for-storage.md`.
- **argparse vs. Click vs. Typer:** Click gewaehlt. Begruendung: siehe `docs/adr/0003-click-for-cli.md`.
- **UUID vs. Auto-Increment-ID:** UUID gewaehlt, da kein gemeinsamer Zaehler noetig und IDs
  stabil bei Import/Export sind.
- **src-Layout vs. Flat Layout:** src-Layout gewaehlt, verhindert versehentliches Importieren
  aus dem Working-Directory statt dem installierten Paket.
