# Sesame Robot – Einkaufsliste für Deutschland

Stand: 31. Oktober 2026. Planungsstand für den DIY-Aufbau mit Lolin/Wemos S2 Mini und selbst gedrucktem Gehäuse (Bambu Lab P1S).

## Ziel und Bezugsstrategie

Zuerst die Grundversion mit acht Servos und OLED-Gesicht bauen, anschließend Abstandssensor und IMU ergänzen, später eventuell eine Kamera.

Möglichst auf drei Händler bündeln:

- **Otronic**: Servos, S2 Mini, OLED und verfügbare Kleinteile; EU-Händler mit Sitz in den Niederlanden und Versand nach Deutschland.
- **Bambu Lab EU**: passender Akku und Ladegerät.
- **Botland**: Spannungswandler und ergänzende Kleinteile.

Dies ist noch kein vollständig verifizierter Warenkorb. Angezeigte Preise aus der Recherche sind unten von Budgetansätzen getrennt. Lieferbestand, Endpreis einschließlich deutscher Umsatzsteuer, Versand, Stecker und mechanische Passung vor der Bestellung prüfen. Die bisher erstellte deutsche PDF liegt diesem Repository nicht bei.

## Grundversion – Hauptteile

| Menge | Teil und Bezugslink | Preis / Budget | Kompatibilität und Hinweise |
| --- | --- | --- | --- |
| 10 | [MG90S Metallgetriebe, 180°, Otronic OT2029-C93](https://www.otronic-shop.de/de/servo-mg90s-micro-metallgetriebe-180-grad) | Angezeigt: 6,50 € je Stück, 65 € zusammen | Acht verbauen, zwei als Ersatz. Alle vom gleichen Typ kaufen. Keine 360°- oder Continuous-Rotation-Ausführung. Servohörner und Schrauben im Lieferumfang prüfen. |
| 1 | [Wemos S2 Mini ESP32-S2, Otronic OT2743](https://www.otronic-shop.de/de/wemos-s2-mini-esp32-s2) | Angezeigt: 6,90 € | USB-C; lose Stiftleisten laut Händler enthalten. Nicht mit ESP8266 D1 Mini oder ESP32-C3 Super Mini verwechseln. |
| 1 | [OLED weiß, 0,96 Zoll, 128×64, I²C, Otronic OT822-C66](https://www.otronic.nl/en/mini-oled-display-white-0-96-inch-128x64-i2c) | Angezeigt: 5,99 € | Vier Anschlüsse, Adresse 0x3C. Platine laut Händler 26,1 × 26,1 × 3,2 mm. SSD1306 und Passung im Deckel vor Bestellung bestätigen. |
| 1 | [Bambu Lab 14500, 7,4 V, 800 mAh, PC003](https://bambulab-eu.myshopify.com/de/products/14500-7-4v-800mah-li-ion-battery-1pcs) | Budgetansatz: 8–12 € | In offizieller Sesame-Stückliste empfohlen; aktuellen Innenrahmen für diesen Akku verwenden. |
| 1 | [Bambu-Ladegerät für 7,4 V mit XH2.54-Anschluss](https://bambulab-eu.myshopify.com/products/7-4v-lithium-battery-charger-with-xh2-54-connector-1pcs) | Budgetansatz: 6–10 € | Passendes Ladegerät zum Akku. Der USB-Anschluss am S2 Mini lädt diesen Akku nicht. |
| 1 | [Pololu D24V50F5, Artikel 2851, 5 V / typisch bis 5 A](https://botland.de/abwartswandler/2754-d24v50f5-abwartswandler-5v-5a-pololu-2851-5903351242752.html) | Budgetansatz: 30–40 € | Empfehlung mit Stromreserve für den handverdrahteten Aufbau; Einbauplatz und isolierte Befestigung selbst vorsehen. Keine bestätigte Drop-in-Passung zu gedruckten Halterungen. |

### Stromversorgung

Die offizielle Stückliste verlangt mindestens **5 V / 3 A an den Versorgungsleitungen**. Acht gleichzeitig bewegte Servos verursachen Lastspitzen. Der größere Wandler bietet Reserve, garantiert aber nicht den Betrieb bei gleichzeitig blockierten Servos; auch Akku und Verkabelung begrenzen die Versorgung.

Das günstige [Otronic-4R7-Modul](https://www.otronic.nl/en/step-down-buck-converter-from-4-5v-24v-to-5v-3a-4r7-adjustable-output) wird mit 3 A maximal beworben, hat laut Detailbeschreibung aber nur **2,1 A Dauerstrom**. Deshalb ist es hier nicht als Standardteil ausgewählt.

Grundschema: **Akku → Schalter → 5-V-Wandler → Servo-Versorgung und 5-V-Eingang des Controllers**. Gemeinsame Masse; keine Motorspeisung über den 3,3-V-Regler des S2 Mini. Vor Anschluss die Ausgangsspannung messen. Akku niemals direkt an Servos oder 5-V-Leitung anschließen. Beim Flashen mit USB Rückspeisung zwischen USB und Akkuversorgung vermeiden; Anschluss gemäß Schaltplan prüfen.

## Grundversion – Kleinteile

Spezifikationen für die Bestellung, noch ohne einzeln verifizierte Händlerangebote. Nach Möglichkeit bei den oben genannten Händlern bündeln.

| Menge | Spezifikation | Hinweis |
| --- | --- | --- |
| 1 | KCD1-Wippschalter, Ein/Aus, einpolig mit zwei Anschlüssen (SPST) | Einbaumaße und Gleichstrombelastbarkeit prüfen; „KCD1“ allein garantiert keine passende Baugröße. |
| 1 | Lochrasterplatine, Raster 2,54 mm, etwa 5 × 7 cm | Für den Einbau passend zuschneiden. |
| 1 | Gerade Stiftleiste, 1 × 40 Pins, Raster 2,54 mm | Daraus acht dreipolige Servoanschlüsse herstellen. |
| je 1 m | Flexible Silikonlitze 22 AWG, rot und schwarz | Für die kurzen Stromversorgungsleitungen gemäß offizieller Anleitung. |
| insgesamt ca. 3 m | Dünne Silikonlitze 30 AWG in mehreren Farben | Signale und OLED; dickere Kabel erschweren den Einbau. |
| 1 Satz | Passendes XH2.54-Gegenstück mit Anschlusslitzen | Polzahl, Kontaktform und Polung am tatsächlichen Bambu-Akku abgleichen. Akkustecker erhalten. |
| 50 | M2 × 5 mm selbstschneidende Schrauben für Kunststoff | Offizielle Stückliste nennt ungefähr 40 Stück. Ein gewöhnliches Maschinenschraubensortiment ersetzt sie nicht. |
| 10 | M2,5 × 5 mm Maschinenschrauben | Laut offizieller Stückliste für Servohornbefestigung; Gewinde an den gelieferten Servos vor Verwendung prüfen. |
| 1 | Elko 1.000 µF, mindestens 10 V | Zusätzliche Pufferung an der 5-V-Schiene; Polarität beachten. |
| je 1 Packung | Schrumpfschlauch und kleine Kabelbinder | Verbindungen isolieren und Kabel bündeln. |
| 1 | USB-C-Datenkabel | Falls vorhanden weiterverwenden; reine Ladekabel eignen sich nicht zum Flashen. |
| nach Bedarf | PLA, 1,75 mm | Vorhandenes Standard-PLA verwenden; Filamentbedarf im Slicer bestimmen. |

Budget für neu gekaufte Kleinteile/Packungen: **25–40 €**. Lötwerkzeug, Multimeter, Schraubendreher und Verbrauchsmaterial zum Löten werden als vorhanden angenommen.

## Gesamtkosten

| Posten | Betrag |
| --- | --- |
| Zehn Servos, S2 Mini, OLED | 77,89 € laut angezeigten Preisen |
| Akku und Ladegerät | 14–22 € Budgetansatz |
| Spannungswandler | 30–40 € Budgetansatz |
| Kleinteile | 25–40 € Budgetansatz |
| Summe vor Versand und Filament | **146,89–179,89 €**, gerundet **150–180 €** |

Die bisherige Schätzung von 100–130 € ist mit dieser Händler- und Wandlerauswahl zu knapp. Mit acht statt zehn Servos spart man zum angezeigten Preis 13 €, hat dann aber keine Ersatzservos. Günstigere Bezugsquellen oder vorhandene Kleinteile können das Budget weiter senken.

## Vor Bestellung und Druck prüfen

- [ ] OLED: SSD1306, 128×64, I²C, vier Anschlüsse; Platinenmaße mit der Deckelaufnahme vergleichen.
- [ ] Servos: ausdrücklich 180°, Metallgetriebe; Maße, Hörner und Schraubengewinde prüfen.
- [ ] Aktuelle Druckdateien mit Innenrahmen für den Bambu-Akku verwenden.
- [ ] Zuerst einen Servositz und die OLED-Aufnahme als Passprobe drucken.
- [ ] Platz für Wandler, Elko, Kabel und Lochrasterplatine einplanen.
- [ ] Akkustecker und Gegenstück anhand tatsächlicher Polzahl und Polarität abgleichen.
- [ ] Schalteröffnung und Schalterabmessungen vergleichen.
- [ ] Tagespreise, deutsche Umsatzsteuer, Lagerbestand und Versand im Warenkorb prüfen.

## Spätere Ausbaustufe 1 – Abstand und Lage

Diese Teile zunächst nicht für die Grundversion bestellen. Preise sind Budgetansätze.

| Menge | Teil | Budget | Einsatz / offene Punkte |
| --- | --- | --- | --- |
| 1 | [VL53L0X als TOF200C-Breakout](https://www.otronic.nl/de/tof200c-vl53l0x-distanzsensor-flugzeit-sehr-genau.html) | 5–10 € | Zuerst vorne; Versorgung und I²C-Pegel des konkreten Breakouts prüfen. |
| 1 | MPU6050 als GY-521-Breakout | 4–8 € | Neigung und Bewegung; konkretes Händlerangebot noch offen. |
| später 2 | Weitere VL53L0X-Breakouts mit herausgeführtem XSHUT | 10–20 € zusammen | Links/rechts; bei mehreren Sensoren I²C-Adressen beim Start über XSHUT getrennt vergeben oder Multiplexer verwenden. |

OLED und Sensoren können grundsätzlich denselben I²C-Bus nutzen, sofern Adressen, Pull-ups und Pegel passen. Signalleitungen am ESP32 müssen mit **3,3-V-Pegeln** arbeiten. Zusätzliche GPIOs und Halterungen bei der Planung berücksichtigen.

Sensoren funktionieren nicht allein durch Anschließen: Firmware um Messungen und Entscheidungen erweitern. Ein erster Ablauf wäre: langsam laufen → Abstand messen → stoppen → drehen → erneut messen → weiterlaufen. Eine IMU liefert Lageinformationen, erzeugt aber allein noch keine aktive Balance oder Navigation.

## Spätere Ausbaustufe 2 – Kamera

| Option | Budgetansatz | Einordnung |
| --- | --- | --- |
| ESP32-CAM mit OV2640 plus passendem ESP32-CAM-MB-USB-Programmieradapter | 15–25 € zusammen | Preiswerte Option für WLAN-Livebild; zusätzlicher Controller, während der S2 Mini die Beine steuert. |
| Seeed Studio XIAO ESP32S3 Sense | 30–35 € | Für spätere eigene Bildverarbeitung; kein direkter Ersatz des S2 Mini ohne Anpassungen. |

Noch keine abschließend ausgewählten Händlerangebote. Beide Optionen benötigen eine eigene Halterung, Firmware und zusätzliche Reserve in der Stromversorgung. Livebild allein ermöglicht noch keine autonome Hinderniserkennung.

## Firmware und Quellen

Für den DIY-Aufbau wird in der offiziellen Anleitung **ESP32Servo 3.0.9** empfohlen; neuere Versionen können unerwünschte Bewegungen anderer Servos auslösen. Die zur gewählten Hardware passende Firmware und Pinbelegung verwenden. Servos vor der endgültigen Montage der Hörner kalibrieren.

- [Offizielle Projektseite](https://www.doriantodd.com/sesame/)
- [Offizielles Repository](https://github.com/dorianborian/sesame-robot)
- [Stückliste](https://github.com/dorianborian/sesame-robot/blob/main/hardware/bom/README.md)
- [Verdrahtung](https://github.com/dorianborian/sesame-robot/blob/main/docs/wiring-guide/README.md)
- [Bauablauf](https://github.com/dorianborian/sesame-robot/blob/main/docs/build-guide/README.md)

Die verlinkte Upstream-Dokumentation kann sich ändern. Händlerangaben sind keine praktische Passungs- oder Belastungsprüfung dieses individuellen Aufbaus.
