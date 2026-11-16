# startrek_farben.py - Farben fuer Star Trek mit Matrix (startrek-m02): vor RUN einmal starten.
# setColors gibt jedem Pixel seine Farbnummer (Namen = Nummern 0-9, oberste Zeile zuerst, links zuerst),
# setPalette macht daraus die gewuenschten Farben. Den Energiebalken (Zeile 7) schaltet das
# Programm nur an und aus; seine Farbe kommt von hier. Karte und Sensor faerbt das Programm selbst.
N = ["schwarz", "rot", "orange", "gelb", "gruen", "tuerkis", "blau", "violett", "magenta", "weiss"]
setColors([N[3]] * 2 + [N[4]] * 6 + ["schwarz"] * 56)   # Zeile 7: Pixel 0-1 Farbe 3, Pixel 2-7 Farbe 4
setPalette(1, (10, 10, 10))   # 1: Enterprise: weiss
setPalette(3, (10, 0, 0))     # 3: Klingone und Energie unter 50: rot
setPalette(4, (0, 10, 0))     # 4: Energie ab 50: gruen
setPalette(5, (0, 0, 10))     # 5: Sternenbasis: blau
setPalette(8, (0, 0, 10))     # 8: Sternenbasis im Sensor: blau
setPalette(7, (10, 8, 0))     # 7: Stern: gelb
setPalette(9, (10, 8, 0))     # 9: Stern: gelb
log("Star-Trek-Farben gesetzt")
