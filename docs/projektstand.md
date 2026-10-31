# Projektstand und Entscheidungen

Stand: 31. Oktober 2026. Grundlage ist der bisherige Chat; kein physischer Baufortschritt wurde bestätigt.

## Ziel

Einen kleinen programmierbaren Roboter selbst bauen, möglichst viele mechanische Teile mit dem vorhandenen Bambu Lab P1S drucken und später einfache autonome Bewegung ermöglichen.

## Verglichene Projekte

| Projekt | Einordnung im bisherigen Vergleich | Entscheidung |
| --- | --- | --- |
| SMARS | Sehr einfaches Roboterfahrzeug | Für das gewünschte Laufroboter-Projekt weniger interessant |
| Otto DIY | Einfacher Zweibeiner mit vier Servos | Weniger mechanische Möglichkeiten als gewünscht |
| AlbertMicro | Einfacher Vierbeiner mit vier Servos und OLED | Als einfachere Alternative betrachtet |
| Sesame Robot | Vierbeiner mit acht Servos, ESP32 und OLED-Gesicht | Aktuell klar bevorzugt |
| XGO-Duck / Microduck | Deutlich komplexer, ungefähr 15 Servos und höhere Kosten | Für den Einstieg zu aufwendig |

Diese Tabelle dokumentiert die bisherige Gesprächsentscheidung und ist kein neu durchgeführter technischer Produktvergleich.

## Gewählter Plan

- Sesame-DIY-Aufbau mit Lolin/Wemos S2 Mini und Handverdrahtung.
- Acht MG90S-180°-Servos; zehn Exemplare für zwei Ersatzservos einplanen.
- 0,96-Zoll-SSD1306-OLED mit 128×64 Pixeln.
- Aktueller Innenrahmen für den Bambu-14500-Akku mit 7,4 V / 800 mAh.
- PLA-Druckteile.
- Zuerst Browsersteuerung und Grundbewegungen, danach Sensorik, anschließend optional Kamera.
- ESP32Servo zunächst in Version 3.0.9 verwenden.

Der Pololu-D24V50F5-Wandler ist eine Empfehlung aus der Einkaufsplanung, noch kein gekauftes oder im Roboter getestetes Teil.

## Tatsächlich dokumentierter Fortschritt

| Bereich | Status |
| --- | --- |
| Ziel und Projektvergleich | Im Gespräch dokumentiert |
| Entscheidung für Sesame | Klare Präferenz des Nutzers; Aufbauplanung darauf ausgerichtet |
| Deutscher Einkaufsentwurf | Erstellt; Preise, Kleinteilangebote und Passung teilweise offen |
| Deutsche Anleitung | Neu als Markdown erstellt; noch nicht praktisch erprobt |
| Frühere PDF „Sesame Robot – Deutsche Bauanleitung“ | Vom Nutzer erwähnt; Datei in dieser Umgebung nicht vorhanden |
| Bestellungen / vorhandene Elektronik | Nicht bestätigt |
| Druckteile | Noch kein abgeschlossener Druck gemeldet |
| Verdrahtung und Zusammenbau | Noch nicht bestätigt |
| Firmware-Build, Upload und Kalibrierung | Noch nicht bestätigt |
| Erster Lauf und Sensortests | Noch nicht bestätigt |

## Budgetentwicklung

Der bisherige Gesprächsansatz lag bei etwa 100–130 €. Mit zehn Servos zum recherchierten Otronic-Preis, hochwertigerem Wandler, Akku, Ladegerät und neu gekauften Kleinteilpackungen liegt die aktuelle Planung bei **150–180 € vor Versand und Filament**. Das ist eine Planung, keine Abrechnung.

## Offene Punkte

- Einzelangebote für Schrauben, Litzen, Akkustecker und weitere Kleinteile endgültig auswählen.
- OLED-Controller und mechanische Aufnahme, Servomaße, Schalter und Wandlerplatz prüfen.
- Warenkorbpreise einschließlich Versand vergleichen.
- Upstream-Commit und zur Hardware passende Firmware-Version festlegen.
- Erfolgreiche Bibliotheks-/Boardpaket-Kombination nach erstem Build festhalten.
- Vorhandene Teile und Werkzeuge ergänzen, sobald bekannt.

## Nächster sinnvoller Schritt

Einkaufsliste vervollständigen und Passproben für Servo/OLED planen. Danach Einkauf, vollständiger Druck, Elektroniktest und Montage gemäß [Bauanleitung](bauanleitung-de.md). Tatsächliche Ergebnisse im [Bauprotokoll](bauprotokoll.md) festhalten.
