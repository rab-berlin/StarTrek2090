# Trefferwahrscheinlichkeit: Phaser trifft bei Zufall 0-15 >= phf * Entfernung, Torpedo bei >= tq; alle 256 Galaxien, 2 Verlaeufe
import sys
from collections import Counter
from players_m2 import play
STRATS = [
    ("Sucher ohne Sensor, Torpedo zuerst", dict(sensor='none', torp='first', refuel=3)),
    ("Scout gerichtet, Phaser zuerst", dict(sensor='dir', torp='need', refuel=5, bsearch=8)),
    ("Scout gerichtet, Mischung", dict(sensor='dir', torp='smart', refuel=5, bsearch=8)),
    ("Scout gerichtet, Torpedo zuerst", dict(sensor='dir', torp='first', refuel=5, bsearch=8)),
    ("Allwissend", dict(omni=True, torp='smart', refuel=3)),
]
for phf, tq in [tuple(map(int, a.split(','))) for a in sys.argv[1:]]:
    for name, kw in STRATS:
        R = Counter(); ph = to = 0
        for D in range(16):
            for E in range(16):
                for sd in range(2):
                    s, p = play(D, E, sd * 1000 + D * 16 + E, phf=phf, tq=tq, **kw)
                    R[s.result] += 1; ph += p.stats['phaser']; to += p.stats['torps']
        n = sum(R.values())
        print(f"phf {phf} tq {tq:2d} | {name:34s} Sieg {R['win']/n:6.1%} Energie {R['energie']/n:6.1%} Zeit {R['zeit']/n:5.1%} | Phaser {ph/n:.1f} Torpedo {to/n:.1f}", flush=True)
