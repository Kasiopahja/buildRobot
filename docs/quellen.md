# Quellen und Versionshinweise

Stand der Planung: 31. Oktober 2026.

## Offizielle Sesame-Unterlagen

- [Projektseite](https://www.doriantodd.com/sesame/)
- [Repository](https://github.com/dorianborian/sesame-robot)
- [Stückliste](https://github.com/dorianborian/sesame-robot/blob/main/hardware/bom/README.md)
- [Druckanleitung und STL-Verweise](https://github.com/dorianborian/sesame-robot/blob/main/hardware/printing/README.md)
- [Bauanleitung mit Montagebildern](https://github.com/dorianborian/sesame-robot/blob/main/docs/build-guide/README.md)
- [Verdrahtung und S2-Mini-Schaltbild](https://github.com/dorianborian/sesame-robot/blob/main/docs/wiring-guide/README.md)
- [Firmware](https://github.com/dorianborian/sesame-robot/tree/main/firmware)
- [Motor-Tests](https://github.com/dorianborian/sesame-robot/tree/main/motor-testing)
- [Wemos S2 Mini – Herstellerdokumentation](https://www.wemos.cc/en/latest/s2/s2_mini.html)

## Umgang mit Versionen

Die Links auf „main“ zeigen einen veränderlichen Stand. Vor Druck und Firmware-Installation einen konkreten Upstream-Commit auswählen und im [Bauprotokoll](bauprotokoll.md) eintragen. Nicht Gehäuseteile, Platinenanleitungen und Firmware verschiedener Hardwarevarianten ungeprüft mischen.

Wichtig für diesen Plan:

- DIY-Handverdrahtung mit S2 Mini.
- Innenrahmen passend zum Bambu-14500-Akkupack.
- ESP32Servo 3.0.9 entsprechend der offiziellen Empfehlung.
- Pinbelegung aus dem zur gewählten Firmware passenden S2-Mini-Schaltbild.

Einige Upstream-Anleitungen enthalten parallel Hinweise zu älteren Akkuhaltern und Distro Boards. Für unseren Plan sind diese Varianten nicht automatisch passend.

## Dateien in diesem Repository

Die deutschen Markdown-Dateien wurden anhand des Chats und verlinkter Projektunterlagen neu zusammengestellt. Sie enthalten eigene Planungsentscheidungen und keine zugesicherte praktische Validierung.

Die frühere PDF „Sesame Robot – Deutsche Bauanleitung“ wurde nicht bereitgestellt. Deshalb ist sie hier nicht enthalten. Am 1. November 2026 wurden elf Original-STLs samt Lizenz, Referenzbildern und Quellenmanifest aus dem fixierten Commit f328ed35f5cbcbdd44a5e16e3ec679d2caa00d92 importiert. [Druckdateien und Blender-Aufbereitung](../hardware/printing/README.md). CAD, Firmware und Schaltbilddateien werden weiterhin über die offiziellen Quellen referenziert.

Händlerlinks und recherchierte Preise stehen direkt in der [Einkaufsliste](einkaufsliste-de.md). Budgetansätze und offene Kompatibilitätsprüfungen sind dort gekennzeichnet.
