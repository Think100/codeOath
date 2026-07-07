# TODO

## Tasks
- [x] Post-Modell mit Titel, Datum, optionalen Tags
- [x] Markdown-Dateien mit Frontmatter laden, kaputte Dateien ueberspringen
      und auf der Startseite melden
- [x] Startseite mit allen Posts, neueste zuerst
- [x] Detailseite pro Post
- [x] Tag-Filter (Klick auf Tag filtert die Liste)
- [x] Tests fuer Domain, Repository und Routen

## Open Questions
- [ ] Sollen Posts mit Datum in der Zukunft ausgeblendet werden (Drafts)?
      Kontext: aktuell werden alle .md-Dateien angezeigt
      Prioritaet: niedrig, erst bei Bedarf

## Resolved
- [x] Posts pro Request neu laden oder cachen? -> Pro Request laden,
      damit Aenderungen an .md-Dateien beim Refresh sichtbar sind
- [x] Frontmatter-Parser selbst schreiben oder Dependency? -> yaml.safe_load
      auf den Block zwischen den --- Zeilen, keine Extra-Dependency
