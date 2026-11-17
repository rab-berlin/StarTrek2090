# Strategien mit den aktuellen Werten (1 Basis, 1 Torpedo, Energie 255, 51 Aktionen, Phaser 16 je Stufe, Flug 4, Sensor 32), alle 256 Galaxien
import statistics, time, sys
from collections import Counter
from players_m2 import play
STRATS = [
    ("Zufall", dict(rand=True)),
    ("Sucher ohne Sensor, Phaser zuerst", dict(sensor='none', torp='need', refuel=3)),
    ("Sucher ohne Sensor, Torpedo zuerst", dict(sensor='none', torp='first', refuel=3)),
    ("Scout, Phaser zuerst", dict(sensor='row', torp='need', refuel=5, bsearch=8)),
    ("Scout, Mischung", dict(sensor='row', torp='smart', refuel=5, bsearch=8)),
    ("Scout, Torpedo zuerst", dict(sensor='row', torp='first', refuel=5, bsearch=8)),
    ("Scout, Mischung, tankt erst beim letzten Pixel", dict(sensor='row', torp='smart', refuel=1, bsearch=8)),
    ("Kenner: Mischung und Gegenzeilen-Regel", dict(sensor='row', torp='smart', refuel=5, bsearch=8, complement=True)),
    ("Allwissend", dict(omni=True, torp='smart', refuel=3)),
]
SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
print("Scout = Sensor je Galaxiezeile, sucht zuerst die Basis, tankt bei 5 Pixeln; Mischung = Phaser, wenn der Klingone in Schusslinie steht, sonst Torpedo")
for name, kw in STRATS:
    R = Counter(); acts = []; ph = to = 0
    for D in range(16):
        for E in range(16):
            for sd in range(SEEDS):
                s, p = play(D, E, sd * 1000 + D * 16 + E, **kw)
                R[s.result] += 1
                if s.result == 'win': acts.append(s.t - 1)
                if p: ph += p.stats['phaser']; to += p.stats['torps']
    n = sum(R.values())
    med = statistics.median(acts) if acts else 0
    print(f"{name:42s} Sieg {R['win']/n:6.1%}  Energie {R['energie']/n:6.1%}  Zeit {R['zeit']/n:6.1%}  Aktionen (Median, Sieg) {med:4.0f}  Phaser {ph/n:4.1f}  Torpedo {to/n:4.1f}", flush=True)
