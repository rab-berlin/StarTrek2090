# startrek_farben.py - Farben fuer Star Trek mit Matrix (startrek-m02): vor RUN einmal starten.
# setColors gibt jedem Pixel seine Farbnummer (Namen = Nummern 0-9, oberste Zeile zuerst, links zuerst),
# setPalette macht daraus die gewuenschten Farben. Den Energiebalken (Zeile 7) schaltet das
# Programm nur an und aus; seine Farbe kommt von hier, ebenso die der Enterprise in der Mitte des Sensors.
# Karte und Nachbarquadranten im Sensor faerbt das Programm selbst.
N = ["schwarz", "rot", "orange", "gelb", "gruen", "tuerkis", "blau", "violett", "magenta", "weiss"]
setColors([N[3]] * 2 + [N[4]] * 6 + ["schwarz"] * 46 + [N[5]] + ["schwarz"] * 9)
# Zeile 7: Pixel 0-1 Farbe 3, Pixel 2-7 Farbe 4; Zeile 1, Spalte 6 (Mitte des Sensors): Farbe 5
setPalette(5, (10, 10, 10))   # 5: Enterprise (Karte und Mitte des Sensors): weiss
setPalette(3, (10, 0, 0))     # 3: Klingone und Energie unter 64: rot
setPalette(4, (0, 10, 0))     # 4: Energie ab 64: gruen
setPalette(7, (0, 0, 10))     # 7: Sternenbasis: blau
setPalette(8, (0, 0, 10))     # 8: Sternenbasis im Sensor: blau
setPalette(11, (7, 0, 10))    # 11: Sensor: Klingone und Basis im selben Quadranten: violett
setPalette(9, (10, 8, 0))     # 9: Stern 1: gelb
setPalette(1, (10, 8, 0))     # 1: Stern 2: gelb
log("Star-Trek-Farben gesetzt")
