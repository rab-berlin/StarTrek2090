# Sensor im Basisquadranten gestoert; alle 256 Verteilungen, 2 Verlaeufe
from collections import Counter
from players_m2 import play
STRATS = [
    ("Sucher ohne Sensor, Torpedo zuerst", dict(sensor='none', torp='first', refuel=3)),
    ("Scout gerichtet, Phaser zuerst", dict(sensor='dir', torp='need', refuel=5, bsearch=8)),
    ("Scout gerichtet, Mischung", dict(sensor='dir', torp='smart', refuel=5, bsearch=8)),
    ("Scout gerichtet, Torpedo zuerst", dict(sensor='dir', torp='first', refuel=5, bsearch=8)),
    ("Scout gerichtet, tankt erst beim letzten Pixel", dict(sensor='dir', torp='smart', refuel=1, bsearch=8)),
]
for name, kw in STRATS:
    R = Counter(); ph = to = se = 0
    for D in range(16):
        for E in range(16):
            for sd in range(2):
                s, p = play(D, E, sd * 1000 + D * 16 + E, **kw)
                R[s.result] += 1; ph += p.stats['phaser']; to += p.stats['torps']; se += p.stats['sensor']
    n = sum(R.values())
    print(f"Basis stoert Sensor | {name:46s} Sieg {R['win']/n:6.1%} Energie {R['energie']/n:6.1%} Zeit {R['zeit']/n:5.1%} | Phaser {ph/n:.1f} Torpedo {to/n:.1f} Scans {se/n:.1f}", flush=True)
