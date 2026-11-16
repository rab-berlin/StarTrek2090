import statistics, time, sys
from collections import Counter
from players_m2 import play
STRATS = [
    ("Zufall", dict(rand=True)),
    ("Sucher (ohne Sensor)", dict(sensor='none', torp='need', refuel=3)),
    ("Sucher, Torpedo zuerst", dict(sensor='none', torp='first', refuel=3)),
    ("Scout (Sensor je Zeile)", dict(sensor='row', torp='need', refuel=3)),
    ("Scout, Torpedo statt Umweg", dict(sensor='row', torp='smart', refuel=3)),
    ("Scout, Sensor in jedem Quadranten", dict(sensor='always', torp='smart', refuel=3)),
    ("Scout, tankt erst bei 1 Pixel", dict(sensor='row', torp='smart', refuel=1)),
    ("Scout, tankt schon bei 5 Pixeln", dict(sensor='row', torp='smart', refuel=5)),
    ("Kenner (Scout + Gegenzeilen-Regel)", dict(sensor='row', torp='smart', refuel=3, complement=True)),
    ("Bester Mensch: Kenner, Torpedo zuerst, tankt bei 5", dict(sensor='row', torp='first', refuel=5, complement=True)),
    ("Allwissend", dict(omni=True, torp='smart', refuel=3)),
]
SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 4
rows = []
for name, kw in STRATS:
    t0 = time.time(); R = Counter(); acts = []; dock = []; ts = []; left = []
    for D in range(16):
        for E in range(16):
            for sd in range(SEEDS):
                s, p = play(D, E, sd * 1000 + D * 16 + E, **kw)
                R[s.result] += 1
                if s.result == 'win': acts.append(s.t - 1); dock.append(sum(1 for l in s.log if l[0] == 'andocken'))
                else: left.append(s.N)
    n = sum(R.values())
    q = statistics.quantiles(acts, n=4) if len(acts) > 3 else [0, 0, 0]
    rows.append((name, R['win'] / n, R['energie'] / n, R['zeit'] / n, R['haengt'] / n, q, statistics.mean(dock) if dock else 0, statistics.mean(left) if left else 0))
    print(f"{name:36s} Sieg {R['win']/n:6.1%}  Energie {R['energie']/n:6.1%}  Zeit {R['zeit']/n:6.1%}  haengt {R['haengt']/n:5.1%}  Aktionen Q1/Med/Q3 {q[0]:.0f}/{q[1]:.0f}/{q[2]:.0f}  Andocken {rows[-1][6]:.1f}  Klingonen uebrig bei Niederlage {rows[-1][7]:.1f}  ({time.time()-t0:.0f}s)", flush=True)
