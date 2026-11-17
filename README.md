# StarTrek2090

Star Trek im Stil von 1971 für den Busch Microtronic 2090 mit dem [ESP2090 Studio](https://github.com/rab-berlin/ESP2090) (8x8-LED-Matrix mit Farben): 8 Klingonen in einer Galaxie aus 16 Quadranten finden und zerstören, bevor Energie oder Zeit ausgehen.

- 252 von 256 Programmschritten belegt
- Dateien: [startrek.mic](startrek.mic), das kommentierte Listing, und das Userscript [startrek_farben.py](startrek_farben.py) für die Farben

![Spielfeld nach einem Sensor-Scan](bilder/spielfeld.png)

## Spiel

Die Galaxie hat 4 x 4 Quadranten zu je 4 x 4 Sektoren und ist ringförmig geschlossen: Wer rechts hinausfliegt, kommt links wieder herein, ebenso oben und unten. Die Matrix zeigt immer nur den Quadranten, in dem die Enterprise gerade steht.

- **Klingonen:** 8, höchstens einer je Quadrant. Sie bewegen sich nicht. Steht die Enterprise in einem Quadranten mit Klingone, schießt er nach jeder Aktion: 0 bis 30 Energie.
- **Basis:** genau eine, irgendwo in der Galaxie. Wer hineinfliegt, dockt an: wieder 255 Energie und 1 Torpedo. Die Enterprise bleibt vor der Basis stehen. Am Anfang hat sie ebenfalls 255 Energie und 1 Torpedo.
- **Sterne:** 2 je Quadrant. Sie halten Flug und Phaser auf.
- **Start:** Die Enterprise startet in der linken unteren Ecke. Liegt dort ein Stern, verdeckt er sie, bis sie losfliegt (in etwa jeder 16. Galaxie).
- **Gewonnen:** alle 8 Klingonen zerstört, das Programm hält an Adresse AF.
- **Verloren:** Energie unter 0 oder nach 51 Aktionen die Zeit abgelaufen, das Programm hält an Adresse B0.

Jede Aktion zählt die Sternzeit weiter, auch Sensor und Andocken. Danach schießt ein Klingone im Quadranten, dann zeichnet die Matrix neu (etwa 3,5 Sekunden).

## Befehle

Jeder Zug beginnt mit einer Taste am Microtronic.

| Taste | Befehl | danach | Kosten | Wirkung |
|---|---|---|---|---|
| 0 | Navigation | Richtung, Entfernung 1-F | 4 Energie je Feld | fliegt Feld für Feld, hält vor Stern oder Klingone; in eine Basis = andocken |
| 1 | Sensor | Richtung | 32 Energie | zeigt den Nachbarquadranten in dieser Richtung und den gegenüberliegenden, bis zur nächsten Aktion |
| 2 | Phaser | Richtung, Energie 1-F | 16 Energie je Stufe | der Strahl fliegt so viele Felder weit und trifft das erste Objekt; einen Klingonen zerstört er auf 1 Feld mit 94 %, auf 2 mit 88 %, auf 3 mit 81 %, je Feld weiter 6 Punkte weniger |
| 3-F | Torpedo | – | 1 Torpedo | zerstört den Klingonen im eigenen Quadranten mit 75 %; ohne Ziel oder Torpedo geschieht nichts |

Richtungen wie auf dem Tastenfeld:

```
8 9 A
4 5 6
0 1 2
```

0 als Entfernung oder Phaser-Energie bricht den Befehl ab, ohne dass Zeit vergeht. Richtung und Entfernung werden nicht angezeigt; erst das neue Bild zeigt, was geschehen ist. Ein Phaser mit F kostet 240 Energie und ist meist das Ende.

## Anzeige

| Wo | Was |
|---|---|
| Matrix, Zeile 7 | Energiebalken, je 32 Energie ein Pixel (8 Pixel = 224 bis 255, 1 Pixel = unter 32). Grün, die letzten beiden rot (unter 64) |
| Matrix, unten links 4 x 4 | der eigene Quadrant: weiß Enterprise, rot Klingone, blau Basis, gelb Sterne |
| Matrix, unten rechts 3 x 3 (Zeilen 0-2, Spalten 5-7) | Sensor: die Quadranten rund um den eigenen (Mitte), oben ist oben in der Galaxie. Es leuchten die beiden gewählten Nachbarn: rot Klingone, blau Basis, violett beides, sonst dunkel |
| Anzeige des Microtronic | beim Warten auf eine Taste drei Ziffern: Sternzeit 0-F, Klingonen übrig, Torpedos. `581` heißt Sternzeit 5, 8 Klingonen, 1 Torpedo. Die Sternzeit rückt alle 3 bis 4 Aktionen eins weiter. Nach F läuft die Zeit ab |

Die Anzeige ist dunkel, solange die Matrix zeichnet: Mit eingeschalteter Anzeige braucht jeder Befehl 20,5 statt 9,3 ms, und dann schafft die Matrix den Handshake nicht.

## Start

1. Matrix einschalten („LED on“ in der Weboberfläche). Sie muss beim Start wach sein.
2. Das Userscript `startrek_farben.py` mit **Run** starten. Es setzt die Farben und endet sofort.
3. RESET, `HALT` `NEXT` `00` `RUN`.

Die Zeit zwischen RESET und RUN bestimmt die Galaxie. Neues Spiel: RESET, RUN.

**Ohne Userscript** färbt das Programm Karte und Sensor selbst, nur der Energiebalken bleibt in der Standardfarbe der Matrix.

## Spieltipps

- Die Enterprise startet in der linken unteren Ecke der Galaxie. Der Sensor zeigt immer zwei gegenüberliegende Nachbarn: Richtung 6 die Galaxiezeile, 9 die Galaxiespalte, 8 und A die Diagonalen. Wer jeweils die Achse mit zwei unbekannten Quadranten wählt, spart viel Suchen.
- Die Klingonen-Reihen der Galaxie sind nicht unabhängig: Von zwei Quadranten derselben Spalte, zwei Galaxiezeilen auseinander, hat genau einer einen Klingonen.
- Die Basis zuerst suchen. Wer sie kennt, kann rechtzeitig tanken; wer sie erst mit leerem Balken sucht, kommt meist nicht mehr an.
- Umwege kosten mehr Energie als alles andere. Lieber früh tanken, beim fünften Pixel, als spät; wer erst beim letzten Pixel losfliegt, kommt fast nie an.
- Ob ein Schuss getroffen hat, zeigt das nächste Bild: Bei einem Treffer verschwindet der rote Punkt, und die Klingonenzahl im Display sinkt. Ein Fehlschuss lässt beides stehen, und der Klingone schießt zurück.
- Phaser und Torpedo ergänzen sich: Steht der Klingone in einer der acht Richtungen frei vor der Enterprise, ist der Phaser die erste Wahl. Sonst spart der Torpedo das Anfliegen einer Schussposition unter Feuer. Jede Basis füllt ihn wieder auf.

## Einstellen

Alle Werte sind Konstanten im Programm und lassen sich ohne zusätzliche Schritte ändern.

| Was | Adresse | Befehl | Bedeutung |
|---|---|---|---|
| Torpedos bei Start und Andocken | 10 | `11C` (`MOVI 1,C`) | `12C` = 2, `13C` = 3 Torpedos |
| Treffer des Torpedos | 6E | `14E` (`MOVI 4,E`) | trifft, wenn der Zufall 0-F mindestens 4 ist: 75 %. `10E` = immer, `18E` = 50 % |
| Zeitlimit | 1E | `55A` (`ADDI 5,A`) | je Aktion + 5, Ende nach 52 Zählungen (51 Aktionen). `54A` = 63, `56A` = 42 Aktionen |
| Energie bei Start und Andocken | 0E, 0F | `1F8`, `1F9` | FFh = 255; der Balken rechnet mit 32 je Pixel |
| Sensor | 7C | `729` (`SUBI 2,9`) | 2 x 16 = 32 Energie |
| Navigation | AC | `748` (`SUBI 4,8`) | 4 Energie je Feld; `738` = 3, `758` = 5 |

## Simulation

Im Ordner [simulation](simulation) liegt ein Regelmodell des Programms in Python mit Spielerstrategien. Die Spieler sehen nur, was auch ein Mensch sieht: den eigenen Quadranten, das Sensorbild, den Energiebalken in 32er-Stufen, Torpedos und Sternzeit. `python3 run_sim.py 1` spielt jede Strategie in allen 256 Verteilungen der Klingonen (einige Sekunden je Strategie); alle Ergebnisse stehen in [sim_ergebnisse.txt](simulation/sim_ergebnisse.txt).

Scout heißt hier: Sensor auf eine Achse mit zwei unbekannten Nachbarquadranten, zuerst die Basis suchen, beim fünften Pixel tanken. Mischung heißt: Phaser, wenn der Klingone in Schusslinie steht, sonst Torpedo.

| Strategie | Siege | verloren durch Energie / Zeit | Schüsse je Partie Phaser / Torpedo |
|---|---|---|---|
| zufällige Tasten | 0 % | 100 % / 0 % | – |
| suchen ohne Sensor | 47 % | 53 % / 0 % | 5,6 / 0,8 |
| Scout, Phaser zuerst (fliegt Schussposition an) | 75 % | 23 % / 1,4 % | 6,8 / 0,5 |
| Scout, Torpedo zuerst | 82 % | 18 % / 0,4 % | 4,3 / 4,0 |
| Scout, Mischung | 80 % | 20 % / 0,4 % | 5,3 / 2,7 |
| Scout, Mischung, tankt erst beim letzten Pixel | 8 % | 92 % / 0 % | 2,0 / 1,5 |
| kennt die ganze Galaxie (obere Grenze) | 94 % | 6 % / 0 % | 6,7 / 2,3 |

Die Werte stammen aus dieser Simulation: eine Basis, 1 Torpedo, 255 Energie, 51 Aktionen, Phaser 16 Energie je Stufe, Flug 4 je Feld, Sensor 32, Torpedo trifft mit 75 %, Phaser mit (16 − Entfernung) / 16. Schüsse zählen mit Fehlschüssen. Mit 255 statt 200 Energie wurde das Spiel um etwa 10 Punkte leichter; die teureren Flüge und der teurere Sensor gleichen das aus. Der Sensor mit wählbarer Richtung macht es für Scouts wieder 7 bis 9 Punkte leichter als ein Sensor nur nach links und rechts; wer gar nicht scannt, gewinnt nur gut jede zweite Partie. Die Fehlschüsse nehmen das wieder um etwa 5 Punkte zurück; wären Phaser auf Entfernung doppelt so unsicher, läge Mischung bei 74 %. Mit 2 oder 3 Torpedos war „Torpedo zuerst“ klar am besten und der Phaser fast überflüssig; mit einem Torpedo liegen alle Kampfstile nah beieinander, und jeder gute Spieler setzt beide Waffen ein. Billigere Phaser machten vor allem das ganze Spiel leichter, auch für planlose Spieler. Mit nur einer Basis war die Basis neben einem Klingonen im Sensor zunächst unsichtbar, und die meisten Partien endeten mit leerem Tank; deshalb zeigt der Sensor „Klingone und Basis“ in einer eigenen Farbe. Die Startaufstellung macht kaum einen Unterschied.

## Wie es gemacht ist

Der 2090 kennt keine indirekte Adressierung und nur eine Rücksprungadresse. 256 Felder Galaxie kann er also weder speichern noch durchsuchen. Deshalb wird die Galaxie bei Bedarf berechnet.

- **Galaxie aus drei Ziffern.** `RND` am Anfang liest den Zähler, der seit RESET läuft. Aus seinen Ziffern D und E entstehen die Klingonen-Reihen D, E, nicht D, nicht E (je ein Bit je Quadrant, zusammen immer 8 Klingonen). Zwei Startwerte, D + F und E, legen für jeden Quadranten die Sektoren von Klingone, Basis und Sternen fest. Die Basis liegt im Quadranten mit der Nummer E. Das ergibt bis zu 4096 verschiedene Galaxien: 256 Verteilungen der Klingonen auf die Quadranten, jede mit 16 Anordnungen innerhalb der Quadranten. Die oberste Ziffer F wächst nur langsam (etwa alle 1,25 Sekunden eins weiter), deshalb hängt die Vielfalt auch davon ab, wie lange man zwischen RESET und RUN wartet.
- **Sensorfarbe gerechnet.** Die Farbe des Sensorpixels ist 8 bei einer Basis, sonst 0; ein Klingone addiert 3. So entstehen rot (3), blau (8) und violett (11) ohne zusätzlichen Befehl.
- **Ein Unterprogramm für alles.** `LQ` (64 Schritte) berechnet zu einem beliebigen Feld den Quadranten und liefert, was auf dem Feld liegt. Flug, Phaser, Sensor und Bild benutzen es alle; der Sensor springt hinter den ersten beiden Befehlen ein und gibt das Feld direkt vor.
- **Reihen drehen statt adressieren.** Die vier Klingonen-Reihen liegen in M0-M3. Um Reihe y zu lesen, dreht das Programm die vier Register, bis sie in M0 liegt, und merkt sich den Drehstand.
- **Energie als Linie.** Der Balken ist ein einziger Linienbefehl der Matrix bis zum Pixel Energie / 32. Das ist die obere Ziffer der Energie, einmal nach rechts geschoben: zwei Befehle statt einer Schleife. Die Farben der Zeile setzt das Userscript; das Programm schaltet die Pixel nur an und aus.
- **Sensor ohne Tabelle.** Die Matrixzeile des Sensors ist dy + 1 (Zeilen 0 bis 2); dieselbe Zahl mal 4 minus 4 ist der Versatz −4, 0 oder +4 zum Nachbarquadranten. Die Gegenrichtung ist 2 minus Zeile und −dx; ein Zähler in R0 sorgt für genau zwei Durchgänge.
- **Ein Würfel für beide Waffen.** Der Phaser merkt sich seine Stufen in R7; beim Treffer ist R7 minus der Rest in R5 die Entfernung. Torpedo und Phaser vergleichen danach dieselbe Zufallszahl aus `RND` mit ihrer Schwelle (4 bzw. Entfernung) und springen bei einem Fehlschuss zurück ins Bild.
- **Torpedo mit Übertrag.** `SUBI 1,C` zieht einen Torpedo ab; war keiner mehr da, macht `ADC C` aus F wieder 0 und lässt den Übertrag stehen, der den Schuss abbricht. Das spart die getrennte Abfrage.
- **Bank offen lassen.** Treffer des Klingonen, Sternzeit und Energiebalken laufen in einem Stück in der Bank (M8-MF). Der Matrixbefehl braucht nur R4 bis R7 und funktioniert deshalb auch dort; das spart vier Bankwechsel und zwei Unterprogramme.
- **Kein Blitzen.** Das Bild zeichnet fünf Pixel nacheinander: Stern 1, Basis, Enterprise, Klingone, Stern 2. Fehlt im Quadranten der Klingone oder die Basis, legt das Programm diesen Eintrag auf Stern 2, der zuletzt kommt und ihn übermalt. So bleibt die Schleife gleich lang, und das Schiff behält immer seine Farbe.
- **Display aus drei Kopien.** Vor dem Warten auf die Taste kopiert das Programm Sternzeit, Klingonen und Torpedos in drei benachbarte Register, die `DISP` dann zeigt. Die Klingonenzahl liegt auf der anderen Registerseite und kommt mit `EXRL; MOV 7,E; EXRL` herüber.
- **Keine verschachtelten Aufrufe.** Das Löschen der Matrix läuft direkt in die Routine für Matrixbefehle hinein, statt sie aufzurufen.

## Geschichte

*Star Trek* schrieb Mike Mayfield 1971 in BASIC: eine Galaxie aus 8 x 8 Quadranten zu je 8 x 8 Sektoren, Klingonen, Sternenbasen, Phaser, Torpedos, Langstreckensensor und eine Sternzeit, bis zu der alle Klingonen zerstört sein müssen. Das Spiel wurde auf vielen Rechnern nachgebaut und gehört zu den bekanntesten Computerspielen der 70er Jahre. Auf dem Microtronic ist die Galaxie auf 4 x 4 x 4 x 4 geschrumpft, und statt eines Bildschirms zeigen 64 LEDs den Quadranten.

---

Ein nicht kommerzielles Fan-Projekt nach dem Computerspiel von 1971; nicht verbunden mit Paramount oder CBS Studios. *Star Trek* und die zugehörigen Namen sind Marken von CBS Studios Inc.
