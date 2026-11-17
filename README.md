# StarTrek2090

Star Trek im Stil von 1971 für den Busch Microtronic 2090 mit dem [ESP2090 Studio](https://github.com/rab-berlin/ESP2090) (8x8-LED-Matrix mit Farben): 8 Klingonen in einer Galaxie aus 16 Quadranten finden und zerstören, bevor Energie oder Zeit ausgehen.

- alle 256 Programmschritte belegt
- Dateien: [startrek.mic](startrek.mic), das kommentierte Listing, und das Userscript [startrek_farben.py](startrek_farben.py) für die Farben

## Spiel

Die Galaxie hat 4 x 4 Quadranten zu je 4 x 4 Sektoren und ist ringförmig geschlossen: Wer rechts hinausfliegt, kommt links wieder herein, ebenso oben und unten. Die Matrix zeigt immer nur den Quadranten, in dem die Enterprise gerade steht.

- **Klingonen:** 8, höchstens einer je Quadrant. Steht die Enterprise in einem Quadranten mit Klingone, schießt er nach jeder Aktion: 0 bis 30 Schaden.
- **Basis:** genau eine, irgendwo in der Galaxie. Wer hineinfliegt, dockt an: wieder 255 Energie und 1 Torpedo. Die Enterprise bleibt vor der Basis stehen. Am Anfang hat sie ebenfalls 255 Energie und 1 Torpedo.
- **Sterne:** 2 je Quadrant. Sie halten Flug und Phaser auf.
- **Start:** Die Enterprise startet in der linken unteren Ecke eines Quadranten der Galaxie.
- **Gewonnen:** alle 8 Klingonen zerstört, bevor der Countdown abgelaufen ist.
- **Verloren:** Energie unter 0 oder der Countdown abgelaufen (51 Aktionen).

Am Ende siehst du auf dem Display das Ergebnis: Klingonen 0 heißt gewonnen, und der Countdown zeigt die übrige Zeit. Countdown 0 heißt, die Zeit ist abgelaufen. Steht beides noch über 0, war die Energie zu Ende. Neues Spiel: RESET, RUN.

Jede Aktion lässt die Zeit weiterlaufen, auch Langstrecken-Sensor und Andocken. Danach schießt ein Klingone im Quadranten, dann zeichnet die Matrix neu.

## Start

1. Matrix einschalten („LED on“ in der Weboberfläche). Sie muss beim Start wach sein.
2. Das Userscript `startrek_farben.py` mit **Run** starten. Es setzt die Farben und endet sofort.
3. RESET, `HALT` `NEXT` `00` `RUN`.

Die Zeit zwischen RESET und RUN bestimmt die Galaxie. Neues Spiel: RESET, RUN.

**Ohne Userscript** färbt das Programm Karte und Langstrecken-Sensor selbst, nur der Energiebalken bleibt in der Standardfarbe der Matrix.

## Anzeige

![Spielfeld nach einem Scan des Langstrecken-Sensors](bilder/spielfeld.png)

| Wo | Was |
|---|---|
| Matrix, Zeile 7 | Energiebalken, je 32 Energie ein Pixel (8 Pixel = 224 bis 255, 1 Pixel = unter 32). Grün, die letzten beiden rot (unter 64) |
| Matrix, unten links 4 x 4 | der eigene Quadrant: weiß Enterprise, rot Klingone, blau Basis, gelb Sterne |
| Matrix, unten rechts 3 x 3 (Zeilen 0-2, Spalten 5-7) | Langstrecken-Sensor: die Quadranten rund um den eigenen (Mitte), oben ist oben in der Galaxie. Es leuchten die beiden gewählten Nachbarn: rot Klingone, blau Basis, violett beides, sonst dunkel |
| Anzeige des Microtronic | beim Warten auf eine Taste und am Ende drei Ziffern: Countdown F-0, Klingonen übrig, Torpedos. `E81` heißt Countdown E, 8 Klingonen, 1 Torpedo. Der Countdown zählt alle 3 bis 4 Aktionen eins herunter; nach 0 ist die Zeit abgelaufen |

Die Anzeige im Display wird ausgeschaltet, solange die Matrix zeichnet.

## Befehle

Jeder Zug beginnt mit einer Taste am Microtronic.

| Taste | Befehl | danach | Kosten | Wirkung |
|---|---|---|---|---|
| 0 | Navigation | Richtung, Entfernung 1-F | 4 Energie je Feld | fliegt Feld für Feld, hält vor Stern oder Klingone; in eine Basis = andocken |
| 1 | Langstrecken-Sensor | Richtung | 32 Energie | zeigt den Nachbarquadranten in dieser Richtung und den gegenüberliegenden, bis zur nächsten Aktion. Im Quadranten der Basis stört die Basis den Langstrecken-Sensor: dort passiert nichts |
| 2 | Phaser | Richtung, Energie 1-F | 16 Energie je Stufe | der Strahl fliegt so viele Felder weit und trifft das erste Objekt; einen nahen Klingonen zerstört er mit höherer, einen fernen mit niedrigerer Wahrscheinlichkeit |
| 3 | Torpedo | – | 1 Torpedo | zerstört den Klingonen im eigenen Quadranten meistens, aber nicht immer; ohne Gegner oder Torpedo geschieht nichts |

Richtungen wie auf dem Tastenfeld:

```
8 9 A
4 5 6
0 1 2
```

0 als Entfernung oder Phaser-Energie bricht den Befehl ab, ohne dass Zeit vergeht. Richtung und Entfernung werden nicht angezeigt; erst das neue Bild zeigt, was geschehen ist. 

Vorsicht: Ein Phaser mit F kostet 240 Energie - die Selbstzerstörung für eine hoffnungslose Lage.

## Spieltipps

- Der Langstrecken-Sensor zeigt immer zwei gegenüberliegende Nachbarn: Richtung 6 die Galaxiezeile, 9 die Galaxiespalte, 8 und A die Diagonalen. Wer jeweils die Achse mit zwei unbekannten Quadranten wählt, spart viel Suchen.
- Im Quadranten der Basis kann man nicht scannen. Wer die Nachbarquadranten der Basis kennen will, scannt vorher oder nachher von außerhalb.
- Die Basis zuerst suchen. Wer sie kennt, kann rechtzeitig tanken; wer sie erst mit leerem Balken sucht, kommt meist nicht mehr an.
- Umwege kosten mehr Energie als alles andere. Lieber früh tanken, beim fünften Pixel, als spät; wer erst beim letzten Pixel losfliegt, kommt fast nie an.
- Ob ein Schuss getroffen hat, zeigt das nächste Bild: Bei einem Treffer verschwindet der rote Punkt, und die Klingonenzahl im Display sinkt. Ein Fehlschuss lässt beides stehen, und der Klingone schießt zurück.
- Phaser und Torpedo ergänzen sich: Steht der Klingone in einer der acht Richtungen frei vor der Enterprise, ist der Phaser die erste Wahl. Sonst spart der Torpedo das Anfliegen einer Schussposition unter Feuer. Jede Basis füllt ihn wieder auf.

## Einstellen

Alle Werte sind Konstanten im Programm und lassen sich ohne zusätzliche Schritte ändern.

| Was | Adresse | Befehl | Bedeutung |
|---|---|---|---|
| Torpedos bei Start und Andocken | 10 | `11C` (`MOVI 1,C`) | `12C` = 2, `13C` = 3 Torpedos |
| Treffer des Torpedos | 71 | `14B` (`MOVI 4,B`) | trifft, wenn der Zufall 0-F mindestens 4 ist. `10B` = immer, höhere Werte = seltener |
| Zeitlimit | 1F | `55A` (`ADDI 5,A`) | je Aktion + 5, Ende nach 52 Zählungen (51 Aktionen). `54A` = 63, `56A` = 42 Aktionen |
| Energie bei Start und Andocken | 0E, 0F | `1F8`, `1F9` | FFh = 255; der Balken rechnet mit 32 je Pixel |
| Langstrecken-Sensor | 7E | `729` (`SUBI 2,9`) | 2 x 16 = 32 Energie |
| Navigation | AE | `748` (`SUBI 4,8`) | 4 Energie je Feld; `738` = 3, `758` = 5 |

## Wie es gemacht ist

Der 2090 kennt keine indirekte Adressierung und nur eine Rücksprungadresse. 256 Felder Galaxie kann er also weder speichern noch durchsuchen. Deshalb wird die Galaxie bei Bedarf berechnet.

- **Galaxie aus drei Ziffern.** `RND` am Anfang liest den Zähler, der seit RESET läuft. Aus seinen Ziffern D und E entstehen die Klingonen-Reihen D, E, nicht D, nicht E (je ein Bit je Quadrant, zusammen immer 8 Klingonen). Deshalb hat von zwei Quadranten derselben Spalte, zwei Galaxiezeilen auseinander, immer genau einer einen Klingonen. Zwei Startwerte, D + F und E, legen für jeden Quadranten die Sektoren von Klingone, Basis und Sternen fest. Die Basis liegt im Quadranten mit der Nummer E. Das ergibt bis zu 4096 verschiedene Galaxien: 256 Verteilungen der Klingonen auf die Quadranten, jede mit 16 Anordnungen innerhalb der Quadranten. Die oberste Ziffer F wächst nur langsam (etwa alle 1,25 Sekunden eins weiter), deshalb hängt die Vielfalt auch davon ab, wie lange man zwischen RESET und RUN wartet.
- **Farben des Langstrecken-Sensors gerechnet.** Die Farbe eines Pixels im Langstrecken-Sensor ist 8 bei einer Basis, sonst 0; ein Klingone addiert 3. So entstehen rot (3), blau (8) und violett (11) ohne zusätzlichen Befehl.
- **Ein Unterprogramm für alles.** `LQ` (64 Schritte) berechnet zu einem beliebigen Feld den Quadranten und liefert, was auf dem Feld liegt. Flug, Phaser, Langstrecken-Sensor und Bild benutzen es alle; der Langstrecken-Sensor springt hinter den ersten beiden Befehlen ein und gibt das Feld direkt vor.
- **Reihen drehen statt adressieren.** Die vier Klingonen-Reihen liegen in M0-M3. Um Reihe y zu lesen, dreht das Programm die vier Register, bis sie in M0 liegt, und merkt sich den Drehstand.
- **Energie als Linie.** Der Balken ist ein einziger Linienbefehl der Matrix bis zum Pixel Energie / 32. Das ist die obere Ziffer der Energie, einmal nach rechts geschoben: zwei Befehle statt einer Schleife. Die Farben der Zeile setzt das Userscript; das Programm schaltet die Pixel nur an und aus.
- **Langstrecken-Sensor ohne Tabelle.** Die Matrixzeile des Langstrecken-Sensors ist dy + 1 (Zeilen 0 bis 2); dieselbe Zahl mal 4 minus 4 ist der Versatz −4, 0 oder +4 zum Nachbarquadranten. Die Gegenrichtung ist 2 minus Zeile und −dx; ein Zähler in R0 sorgt für genau zwei Durchgänge.
- **Ein Würfel für beide Waffen.** Der Phaser merkt sich seine Stufen in R7; beim Treffer ist R7 minus der Rest in R5 die Entfernung. Torpedo und Phaser legen ihre Schwelle (4 bzw. Entfernung) in RB ab und teilen sich den Trefferwurf: `RND`, Vergleich, bei einem Fehlschuss zurück ins Bild. Ob der Phaser überhaupt einen Klingonen erreicht hat, prüft `SUBI F,F`: nur bei F borgt es nicht.
- **Torpedo mit Übertrag.** `SUBI 1,C` zieht einen Torpedo ab; war keiner mehr da, macht `ADC C` aus F wieder 0 und lässt den Übertrag stehen, der den Schuss abbricht. Das spart die getrennte Abfrage.
- **Bank offen lassen.** Treffer des Klingonen, Sternzeit und Energiebalken laufen in einem Stück in der Bank (M8-MF). Der Matrixbefehl braucht nur R4 bis R7 und funktioniert deshalb auch dort; das spart vier Bankwechsel und zwei Unterprogramme.
- **Kein Blitzen.** Das Bild zeichnet fünf Pixel nacheinander: Stern 1, Basis, Enterprise, Klingone, Stern 2. Fehlt im Quadranten der Klingone oder die Basis, legt das Programm diesen Eintrag auf Stern 2, der zuletzt kommt und ihn übermalt. So bleibt die Schleife gleich lang, und das Schiff behält immer seine Farbe.
- **Display aus drei Kopien.** Vor dem Warten auf die Taste kopiert das Programm Countdown (`INV` der Sternzeit), Klingonen und Torpedos in drei benachbarte Register, die `DISP` dann zeigt. Die Klingonenzahl liegt auf der anderen Registerseite und kommt mit `EXRL; MOV 7,E; EXRL` herüber.
- **Ende ohne HALT.** Jedes Spielende springt in eine Schleife, die nur `DISP` zeigt. Damit das Display dort noch stimmt, holt der Gegenschuss seine Zufallszahl, bevor er in die Registerbank wechselt, und lässt die drei Display-Register in Ruhe. Alle tödlichen Abzüge prüfen den Übertrag noch in der Bank.
- **Keine verschachtelten Aufrufe.** Das Löschen der Matrix läuft direkt in die Routine für Matrixbefehle hinein, statt sie aufzurufen.

## Geschichte

*Star Trek* schrieb Mike Mayfield 1971 in BASIC: eine Galaxie aus 8 x 8 Quadranten zu je 8 x 8 Sektoren, Klingonen, Sternenbasen, Phaser, Torpedos, Langstreckensensor und eine Sternzeit, bis zu der alle Klingonen zerstört sein müssen. Das Spiel wurde auf vielen Rechnern nachgebaut und gehört zu den bekanntesten Computerspielen der 70er Jahre. Auf dem Microtronic ist die Galaxie auf 4 x 4 x 4 x 4 geschrumpft, und statt eines Bildschirms zeigen 64 LEDs den Quadranten.

---

Ein nicht kommerzielles Fan-Projekt nach dem Computerspiel von 1971; nicht verbunden mit Paramount oder CBS Studios. *Star Trek* und die zugehörigen Namen sind Marken von CBS Studios Inc.
