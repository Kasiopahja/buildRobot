# Sesame Robot – Deutsche Bauanleitung

Stand: 31. Oktober 2026. Arbeitsanleitung für unseren geplanten DIY-Aufbau mit S2 Mini, acht MG90S-180°-Servos, SSD1306-OLED und Bambu-Akku.

Diese Fassung wurde für dieses Repository neu zusammengestellt. Sie ist nicht die früher erwähnte PDF und keine vollständige Übersetzung der offiziellen Anleitung. Schaltbilder, Pinbelegung, Servonummerierung und Montagebilder immer aus der zur Hardware passenden offiziellen Version übernehmen. Der eigene Aufbau wurde noch nicht praktisch erprobt.

## 1. Vorbereitung

- [Einkaufsliste](einkaufsliste-de.md) und [Projektstand](projektstand.md) lesen.
- Die [offizielle Bauanleitung](https://github.com/dorianborian/sesame-robot/blob/main/docs/build-guide/README.md), [Stückliste](https://github.com/dorianborian/sesame-robot/blob/main/hardware/bom/README.md) und [Verdrahtung](https://github.com/dorianborian/sesame-robot/blob/main/docs/wiring-guide/README.md) öffnen.
- Mit dem empfohlenen **S2-Mini-Aufbau mit Handverdrahtung** arbeiten. Anweisungen für Distro Boards V1/V2/V3 nicht ungeprüft übertragen.
- Verwendeten Upstream-Commit, Druckdateinamen und später die Bibliotheksversionen im [Bauprotokoll](bauprotokoll.md) festhalten.
- Lötstation, Multimeter, Seitenschneider, Abisolierhilfe, kleine Schraubendreher und eine freie Arbeitsfläche vorbereiten.

## 2. Druck auf dem Bambu Lab P1S

Seit 1. November 2026 liegen [Originale und mit Blender ausgerichtete Druckplatten](../hardware/printing/README.md) im Repository. Dort stehen auch die Hinweise für den vom Nutzer bevorzugten PETG-Druck. Eine gemeinsame 3MF-Platte enthält jedes der elf Teile einmal; alternativ sind zehn Grundteile und ein separater Deckel vorbereitet. Die Dateien enthalten keine fertigen Slicerprofile.

Die [offizielle Druckanleitung](https://github.com/dorianborian/sesame-robot/blob/main/hardware/printing/README.md) nennt PLA/PLA+, zwei Wände und 8–10 % Honeycomb-Infill. Die acht Gelenkteile, der Innenrahmen und die Bodenplatte sind dort ohne Stützen vorgesehen; der Deckel braucht gezielte Stützen.

Als **eigener Startpunkt**, nicht als zusätzlich verifizierte Projektvorgabe: 0,4-mm-Düse, 0,2-mm-Schichthöhe und das zum PLA passende Bambu-Studio-Materialprofil. Bauteile in Originalgröße drucken. Deckelstützen anhand der Bilder zur gewählten Deckelvariante setzen und die Vorschau prüfen.

1. Aktuelle zusammenpassende STL-Dateien auswählen, insbesondere den Innenrahmen für den Bambu-14500-Akku.
2. Zuerst einen Servositz und die OLED-Aufnahme als Passprobe drucken.
3. Servo, Display und Schalter ohne Gewalt einsetzen; bei Abweichungen die Aufnahme gezielt anpassen.
4. Erst danach alle acht Gelenkteile, Rahmen, Boden und einen Deckel drucken.
5. Stützen, Grate und Fäden entfernen. Schraublöcher vorsichtig prüfen; selbstschneidende Schrauben nicht überdrehen.
6. Dateiversionen, Filamentverbrauch und Anpassungen protokollieren.

## 3. Elektronik außerhalb des Gehäuses vorbereiten

Akku und USB vor Lötarbeiten trennen. Zuerst alle Teile auf der Arbeitsfläche anordnen und den Kabelweg planen.

- Servoanschlüsse mit S0 bis S7 beschriften; Position und Signal-GPIO aus dem offiziellen S2-Mini-Schaltbild übernehmen.
- Lochrasterplatine auf Einbaugröße bringen. Keine unisolierten Leiterbahnen auf andere Bauteile legen.
- Kurze Stromversorgungsleitungen aus 22-AWG-Litze aufbauen; für Signale die dünne 30-AWG-Litze verwenden.
- Plus, Masse und Signal an jedem Servoanschluss einzeln abgleichen. Kabelfarben allein ersetzen die Anschlussprüfung nicht.
- Anschlüsse für OLED, Schalter und Akku so vorsehen, dass sie beim Einbau nicht unter Zug stehen.
- Polung und Kontaktbelegung des Akku-Gegenstücks prüfen; den werkseitigen Akkustecker erhalten.

Für den Pololu-Wandler ist eine eigene isolierte Montage einzuplanen. Gehäusekontakt, Klebstoff oder Schrumpfschlauch dürfen die notwendige Wärmeabfuhr nicht unberücksichtigt lassen.

## 4. Versorgung und Verdrahtung prüfen

Schema für diesen Aufbau:

```text
7,4-V-Akkupack
    |
  Schalter
    |
5-V-Step-down
    +---- Servo-Plusleitungen
    +---- 5-V-Eingang S2 Mini

Gemeinsame Masse: Akku / Wandler / S2 Mini / Servos
OLED: Versorgung und SDA/SCL gemäß S2-Mini-Schaltbild
```

Das Schema ist eine Funktionsübersicht, kein vollständiger Anschlussplan. Die genaue Pinbelegung ist in [Quellen und Versionshinweisen](quellen.md) verlinkt.

1. Ohne angeschlossene Versorgung auf Kurzschlüsse und vertauschte Leitungen prüfen.
2. Wandler zunächst ohne Controller und Servos betreiben und etwa 5 V am Ausgang messen.
3. Versorgung wieder trennen, dann Controller und OLED anschließen.
4. Display-Versorgung entsprechend dem Modul wählen und sicherstellen, dass SDA/SCL keine 5-V-Pull-ups zum ESP32 führen.
5. Servos erst nach Prüfung der Leitungen anschließen. Der 3,3-V-Regler des Controllers versorgt keine Servos.
6. Bei externen 5 V und USB auf mögliche Rückspeisung achten; für Flash-Arbeiten die Akkuversorgung trennen, bis die konkrete Stromführung geprüft ist.

Den Akku mit seinem passenden Ladegerät laden. Ein vollständig geladener 2S-Li-ion-Akku liegt oberhalb seiner Nennspannung von 7,4 V; er darf nicht direkt an die 5-V-Schiene.

## 5. Firmware vorbereiten und flashen

- Arduino IDE und das ESP32-Boardpaket von Espressif installieren.
- **LOLIN S2 Mini** als Board auswählen.
- Firmware und alle zugehörigen Dateien aus dem [offiziellen Firmware-Verzeichnis](https://github.com/dorianborian/sesame-robot/tree/main/firmware) zusammen herunterladen.
- Im Bibliotheksmanager **ESP32Servo 3.0.9** fest auswählen. Die offizielle Projektseite warnt bei neueren Versionen vor gegenseitig beeinflussten Servos.
- Weitere Bibliotheken und USB-Einstellungen anhand der README der verwendeten Firmware-Version einrichten; die tatsächlich funktionierenden Versionen protokollieren.
- Zuerst die zur S2-Mini-Pinbelegung passende Motor-Testfirmware verwenden. Keine Distro-Board-Pinbelegung übernehmen.
- Ein USB-Datenkabel verwenden. Bei Uploadproblemen Boot-/Reset-Verfahren anhand der Boardanleitung prüfen.
- Anschließend die vollständige Firmware mit Bewegungen und Gesicht installieren.

Die vorhandene Firmware wird hier noch nicht kopiert oder verändert. Die endgültige Versionsauswahl und ein erfolgreicher Build sind noch offen.

## 6. Servos testen und kalibrieren

**Gelenke und Hörner noch nicht endgültig auf die Servoachsen montieren.** Die Achsen müssen für den ersten Test frei beweglich sein.

1. Jeden Servo einzeln testen und defekte oder auffällige Exemplare aussortieren.
2. Zuordnung von S0–S7 zu Anschluss und Position kontrollieren.
3. Die Referenzstellung der offiziellen Test-/Kalibrieranleitung anfahren.
4. Passende Gelenke entsprechend der dort gezeigten Orientierung aufsetzen; linke und rechte Teile nicht vertauschen.
5. Befestigungsschraube passend zum tatsächlichen Achsgewinde wählen. Nicht gegen Widerstand eindrehen.
6. Bewegungsbereich vorsichtig prüfen, bevor alle Gelenke endgültig befestigt werden.
7. Bei Anschlägen, starkem Brummen oder übermäßiger Erwärmung sofort stoppen und die Ausrichtung korrigieren.

Ein pauschaler 90°-Befehl ersetzt nicht die Sesame-spezifische Referenzstellung.

## 7. Zusammenbau und erster Lauf

Controller, Wandler und Kabel so befestigen, dass der USB-Port erreichbar bleibt. Leitungen von Gelenken fernhalten, Lötstellen isolieren und nichts unter dem Deckel einklemmen. Erst schließen, wenn die offenen Funktionstests erfolgreich sind.

Zum ersten Bewegungstest den Körper abstützen, sodass die Beine frei arbeiten können. Zuerst Ruhe- und Standpose, dann kurze Bewegungen auf freier ebener Fläche testen. Akku- und 5-V-Spannung unter Bewegung beobachten.

Die Firmware stellt eine WLAN-/Browsersteuerung bereit. Den tatsächlichen Zugangspunkt und die Adresse aus der verwendeten Firmware entnehmen. Zugangsdaten nicht in dieses Repository schreiben.

## 8. Typische Fehler

| Symptom | Zuerst prüfen |
| --- | --- |
| Neustart beim Bewegen | 5-V-Versorgung unter Last, Akkuladung, Leitungen und Steckkontakte; Wandler-Dauerstrom statt nur Werbe-Maximalstrom |
| Servo läuft falsch oder schlägt an | Anschlussnummer, linkes/rechtes Gelenk, Referenzstellung und Hornorientierung |
| Mehrere Servos reagieren unerwartet | ESP32Servo-Version 3.0.9, Pinbelegung und gemeinsame Masse |
| OLED bleibt dunkel | Versorgung, SDA/SCL, I²C-Adresse, SSD1306-Ausführung und Lötstellen |
| Kein Upload möglich | Datenkabel, Boardauswahl, Port und Boot-/Reset-Verfahren |
| Deckel lässt sich nicht schließen | Platinenabmessungen, Wandlerhöhe, Stecker und Kabelwege |
| Schraube greift nicht | Tatsächliches Servo-Gewinde beziehungsweise selbstschneidender Schraubentyp |

Sensoren und Kamera erst nach bestandener Grundinbetriebnahme ergänzen: siehe [Ausbauplan](ausbauplan.md).
