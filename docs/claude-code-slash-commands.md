# Claude Code — Slash Commands Cheatsheet

> **Version:** 1.0.0
> **Datum:** 2026-02-22 19:16 (Vienna)

---

## Eingebaute Slash-Befehle

| Befehl | Beschreibung |
|--------|-------------|
| `/help` | Zeigt die Nutzungshilfe an |
| `/exit` | Beendet Claude Code |
| `/clear` | Löscht die gesamte Konversationshistorie |
| `/compact [anweisungen]` | Komprimiert die Konversation, optional mit Fokus-Anweisungen |
| `/config` | Öffnet die Einstellungsoberfläche |
| `/context` | Visualisiert die aktuelle Kontextnutzung als farbiges Gitter |
| `/copy` | Kopiert die letzte Assistenten-Antwort in die Zwischenablage |
| `/cost` | Zeigt Token-Verbrauch und Kosten an |
| `/debug [beschreibung]` | Fehlerbehebung der aktuellen Session via Debug-Log |
| `/desktop` | Übergibt die CLI-Session an die Claude Code Desktop-App (macOS/Windows) |
| `/doctor` | Prüft die Gesundheit der Claude Code Installation |
| `/export [dateiname]` | Exportiert die Konversation in eine Datei oder Zwischenablage |
| `/fast` | Schaltet den Fast-Modus um (schnellere Ausgabe, gleiches Modell) |
| `/init` | Initialisiert ein Projekt mit einer `CLAUDE.md` Datei |
| `/mcp` | Verwaltet MCP-Server-Verbindungen und OAuth-Authentifizierung |
| `/memory` | Bearbeitet die `CLAUDE.md` Speicherdateien |
| `/model` | Wechselt das KI-Modell (+ Pfeiltasten für Anstrengungsstufe) |
| `/permissions` | Zeigt oder aktualisiert Berechtigungseinstellungen |
| `/plan` | Aktiviert den Plan-Modus direkt aus der Eingabe |
| `/rename <name>` | Benennt die aktuelle Session um |
| `/resume [session]` | Setzt eine frühere Session fort (per ID, Name oder Picker) |
| `/rewind` | Setzt die Konversation/Code zurück oder fasst ab einem Punkt zusammen |
| `/stats` | Zeigt Nutzungsstatistiken, Session-Verlauf und Serien |
| `/status` | Zeigt Version, Modell, Konto und Konnektivität |
| `/statusline` | Richtet die Status-Zeilen-UI ein |
| `/tasks` | Listet Hintergrund-Tasks auf und verwaltet sie |
| `/teleport` | Setzt eine Remote-Session von claude.ai fort (nur Abonnenten) |
| `/theme` | Ändert das Farbschema |
| `/todos` | Zeigt aktuelle TODO-Elemente an |
| `/usage` | Zeigt Nutzungsgrenzen und Rate-Limit-Status (nur Abo-Pläne) |
| `/vim` | Aktiviert den Vim-Bearbeitungsmodus |

---

## Spezielle Eingabe-Präfixe

| Präfix | Funktion |
|--------|----------|
| `!befehl` | Bash-Modus — führt Shell-Befehle direkt aus und fügt Ausgabe zur Session hinzu |
| `@datei` | Dateipfad-Erwähnung mit Autocompletion |

---

## Wichtige Tastenkombinationen

| Tastenkombination | Funktion |
|-------------------|----------|
| `Ctrl+C` | Bricht aktuelle Eingabe/Generierung ab |
| `Ctrl+D` | Beendet die Session |
| `Ctrl+F` | Beendet alle Hintergrund-Agents (2x innerhalb 3s bestätigen) |
| `Ctrl+L` | Löscht den Terminal-Bildschirm (Konversation bleibt erhalten) |
| `Ctrl+O` | Schaltet ausführliche Ausgabe um |
| `Ctrl+B` | Setzt laufende Tasks in den Hintergrund |
| `Ctrl+T` | Schaltet die Task-Liste um |
| `Ctrl+V` / `Cmd+V` | Fügt ein Bild aus der Zwischenablage ein |
| `Shift+Tab` / `Alt+M` | Wechselt zwischen Permission-Modi |
| `Alt+P` / `Option+P` | Wechselt das Modell |
| `Alt+T` / `Option+T` | Schaltet Extended Thinking um |
| `Esc` + `Esc` | Rewind — Konversation zurückspulen/zusammenfassen |

---

## Hinweise

- Zusätzlich zu den eingebauten Befehlen können **benutzerdefinierte Skills** (z.B. `/sync`, `/keybindings-help`) projektspezifisch konfiguriert werden.
- Der `/fast`-Modus verwendet dasselbe Claude Opus 4.6 Modell — nur die Ausgabegeschwindigkeit wird erhöht.
- Mit `/model` und den Pfeiltasten (Links/Rechts) kann die **Anstrengungsstufe** (Reasoning Effort) angepasst werden.

---

> Erstellt: 2026-02-22 19:16 Uhr (Vienna)
