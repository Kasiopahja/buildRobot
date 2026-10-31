# Ausbauplan und Aufgaben

Stand: 31. Oktober 2026. Aufgaben sind bewusst offen, bis ihre Ausführung bestätigt wurde.

## Phase 1 – Grundversion

- [ ] Vorhandene Werkzeuge und Teile erfassen.
- [ ] Hauptteile und Kleinteile einschließlich Versand endgültig auswählen.
- [ ] OLED, Servo, Schalter, Stecker und Wandler mechanisch/elektrisch abgleichen.
- [ ] Verwendeten Upstream-Commit und STL-Versionen dokumentieren.
- [ ] Passproben drucken.
- [ ] Alle benötigten Druckteile fertigen und nacharbeiten.
- [ ] Versorgung aufbauen und 5 V messen.
- [ ] Controller und OLED testen.
- [ ] Firmware für S2 Mini mit ESP32Servo 3.0.9 bauen und flashen.
- [ ] Acht Servos einzeln testen, zuordnen und kalibrieren.
- [ ] Mechanik und Elektronik montieren.
- [ ] Stand-/Ruhepose, kurze Laufbewegung und Drehung testen.
- [ ] Akkubetrieb unter Bewegung ohne Neustarts prüfen.
- [ ] Gehäuse schließen und Konfiguration dokumentieren.

Ergebnis dieser Phase: ein zuverlässig per Browser steuerbarer Roboter. Sensoren und Kamera sind dafür nicht erforderlich.

## Phase 2 – Ein Abstandssensor und IMU

- [ ] VL53L0X-Breakout und MPU6050/GY-521 auswählen.
- [ ] 3,3-V-I²C-Pegel, Adressen und freie Anschlüsse prüfen.
- [ ] Halterungen entwerfen und drucken.
- [ ] Sensoren zuerst auf dem Tisch auslesen.
- [ ] Messwerte bei laufenden Servos prüfen.
- [ ] Neigungswerte filtern und Grenzwerte erproben.
- [ ] Hindernisreaktion mit langsamer Bewegung implementieren.
- [ ] Bei ungültigen/ausbleibenden Abstandsmessungen anhalten.

Erster autonomer Ablauf: kurz vorwärtslaufen → messen → bei Hindernis stoppen → drehen → erneut messen. Die Stoppschwelle muss Gehgeschwindigkeit, Messintervall und tatsächlichen Anhalteweg berücksichtigen. Ein vorderer ToF-Sensor erkennt keine Treppenabgründe zuverlässig.

## Phase 3 – Links/rechts messen

- [ ] Zwei weitere VL53L0X mit zugänglichem XSHUT ergänzen.
- [ ] Unterschiedliche I²C-Adressen beim Start vergeben oder Multiplexer einplanen.
- [ ] Blickrichtungen und tote Winkel prüfen.
- [ ] Die freiere Richtung auswählen; wiederholtes Hin-und-her-Drehen vermeiden.
- [ ] Bei fehlendem freien Weg anhalten.

## Phase 4 – Optionale Kamera

- [ ] Für WLAN-Livebild: ESP32-CAM/OV2640 plus passender Programmieradapter prüfen.
- [ ] Für eigene Bildverarbeitung: XIAO ESP32S3 Sense gesondert bewerten.
- [ ] Kamera als zusätzlichen Controller planen, sofern kein bewusster Firmware-Umbau erfolgt.
- [ ] Versorgung, Gewicht, Befestigung und WLAN-Betrieb testen.
- [ ] Erst danach Kameraergebnisse mit der Bewegungssteuerung verknüpfen.

## Später

Mikrofon/Lautsprecher und weitere Interaktionen erst nach stabiler Mechanik und Stromversorgung bewerten. Für die Grundversion keine zusätzliche Hardware allein für hypothetische spätere Funktionen kaufen.
