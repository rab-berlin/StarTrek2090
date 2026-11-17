# players_m2.py - Spielerstrategien fuer startrek-m02 auf dem Regelmodell sim_m2.Sim
# Die Spieler (ausser "allwissend") sehen nur, was auch der Mensch sieht: den eigenen Quadranten,
# das Sensorbild, den Energiebalken (25er-Stufen), Torpedos und Sternzeit.
import random
from collections import deque
from sim_m2 import Sim, DIRS, VEC

MOVES = [(d, v) for d, v in DIRS.items()]


class Player:
    def __init__(self, sim, sensor='none', torp='need', refuel=3, complement=False, omni=False, margin=2, bsearch=None):
        self.s = sim
        self.sensor_mode, self.torp_mode, self.refuel = sensor, torp, refuel
        self.complement, self.omni, self.margin = complement, omni, margin
        self.bsearch = refuel + 1 if bsearch is None else bsearch
        self.pair = sim.bases == 2      # Regel: zweite Basis 2 Zeilen weiter
        self.known = {}          # Zelle -> Code (0 frei, 1 Hindernis, 8 Basis, 15 Klingone)
        self.qk = {}             # Quadrant -> 'K' / '-' (kein Klingone)
        self.bases = set()       # Quadranten mit Basis
        self.bseen = set()       # Quadranten, deren Basis-Status bekannt ist
        self.scanned_rows = set()
        self.stats = dict(dock=0, torps=0, sensor=0, phaser=0, nav=0)

    # ---------- Wissen
    def see(self):
        s = self.s
        if self.omni:
            for x in range(16):
                for y in range(16):
                    self.known[x, y] = s.cell(x, y)
            for qx in range(4):
                for qy in range(4):
                    q = s.ref.quad(qx, qy)
                    self.qk[qx, qy] = 'K' if q['kal'] else '-'
                    if q['base']: self.bases.add((qx, qy))
            return
        vis = s.visible()
        self.known.update(vis)
        q = (s.x >> 2, s.y >> 2)
        k = any(c == 15 for c in vis.values())
        self.set_q(q, 'K' if k else '-')
        if any(c == 8 for c in vis.values()): self.add_base(q)
        self.no_base(q)
        if s.sens:
            for qq, v in s.sens.items():
                if v in ('K', 'KB'):
                    self.set_q(qq, 'K')
                    if v == 'KB': self.add_base(qq)
                else:
                    self.set_q(qq, '-')
                    if v == 'B': self.add_base(qq)
                    self.no_base(qq)

    def set_q(self, q, v):
        old = self.qk.get(q)
        self.qk[q] = v
        if self.complement:
            o = (q[0], (q[1] + 2) & 3)
            if v == 'K' and o not in self.qk: self.qk[o] = '-'
            if v == '-' and old is None and o not in self.qk:
                self.qk[o] = 'K'

    def no_base(self, q):
        self.bseen.add(q)
        if self.pair: self.bseen.add((q[0], (q[1] + 2) & 3))

    def add_base(self, q):
        self.bases.add(q)
        if self.pair: self.bases.add((q[0], (q[1] + 2) & 3))
        else: self.bseen.update((qx, qy) for qx in range(4) for qy in range(4))

    # ---------- Wege (Befehlsfolgen, eine Aktion je gerader Strecke)
    def plan(self, goal, through_goal=False, cmd_cost=4):
        """Billigste Befehlsfolge zu einer Zielzelle (Flugkosten je Feld + cmd_cost je Befehl).
        Unbekannte Zellen gelten als frei."""
        import heapq
        s = self.s
        st = (s.x, s.y)
        if goal(st) and not through_goal: return []
        best = {st: 0}; prev = {st: None}
        import itertools
        cnt = itertools.count()
        h = [(0, 0, st)]
        while h:
            cost, _, c = heapq.heappop(h)
            if cost > best.get(c, 1e9): continue
            if c[0] == 'END':
                c = c[1]; path = [prev[('END', c)][1]]
                cc = prev[('END', c)][0]
                while prev[cc]: cc, m = prev[cc]; path.append(m)
                return path[::-1]
            if c != st and not through_goal and goal(c):
                path = []
                while prev[c]: c, m = prev[c]; path.append(m)
                return path[::-1]
            for d, (dx, dy) in MOVES:
                for n in range(1, 16):
                    nx, ny = (c[0] + n * dx) & 15, (c[1] + n * dy) & 15
                    code = self.known.get((nx, ny), 0)
                    nc = cost + s.navcost * n + cmd_cost
                    if code:
                        if through_goal and goal((nx, ny)):
                            key = ('END', (nx, ny))
                            nc -= s.navcost
                            if nc < best.get(key, 1e9):
                                best[key] = nc; prev[key] = (c, (d, n)); heapq.heappush(h, (nc, next(cnt), key))
                        break
                    if nc < best.get((nx, ny), 1e9):
                        best[nx, ny] = nc; prev[nx, ny] = (c, (d, n)); heapq.heappush(h, (nc, next(cnt), (nx, ny)))
        return None

    def go(self, path):
        """Ersten Befehl der Befehlsfolge ausfuehren; Blockade lernen."""
        d, n = path[0]
        s = self.s
        x0, y0 = s.x, s.y
        dx, dy = DIRS[d]
        s.nav(d, n)
        self.stats['nav'] += 1
        moved = max(abs(((s.x - x0 + 8) & 15) - 8), abs(((s.y - y0 + 8) & 15) - 8))
        if moved < n and self.s.energy >= 0:
            bx, by = (s.x + dx) & 15, (s.y + dy) & 15
            if not self.known.get((bx, by)): self.known[bx, by] = 1
        return True

    # ---------- Kampf
    def shots(self, kx, ky):
        """Feuerstellungen: Zelle -> (Richtung, Stufe), Weg frei (nach bekanntem Wissen)."""
        out = {}
        for d, (dx, dy) in MOVES:
            for k in range(1, 4):
                px, py = (kx - k * dx) & 15, (ky - k * dy) & 15
                if self.known.get((px, py), 0) not in (0,) and (px, py) != (self.s.x, self.s.y): break
                if (px, py) not in self.known: break
                if all(self.known.get(((px + j * dx) & 15, (py + j * dy) & 15), 1) == 0 for j in range(1, k)):
                    out.setdefault((px, py), (d, k))
        return out

    def est_energy(self):
        return self.s.bar_low()          # vorsichtig: untere Grenze des Balkens

    def fight(self):
        s = self.s
        kx, ky = next(c for c, v in s.visible().items() if v == 15)
        sh = self.shots(kx, ky)
        here = sh.get((s.x, s.y))
        e = self.est_energy()
        if self.torp_mode == 'first' and s.torps:
            self.stats['torps'] += 1; return s.torp()
        if here and e >= s.phcost(here[1]) + 16 * self.margin:
            self.stats['phaser'] += 1; return s.phaser(*here)
        if s.torps and (self.torp_mode == 'smart' or e < 16 * 2 + 16 * self.margin):
            self.stats['torps'] += 1; return s.torp()
        qx, qy = kx >> 2, ky >> 2
        good = {c for c, v in sh.items() if e >= s.phcost(v[1]) + 16 * self.margin and (c[0] >> 2, c[1] >> 2) == (qx, qy)}
        p = self.plan(lambda c: c in good) if good else None
        if p:
            return self.go(p)
        if s.torps:
            self.stats['torps'] += 1; return s.torp()
        return None

    # ---------- ein Zug
    def step(self):
        s = self.s
        self.see()
        here = (s.x >> 2, s.y >> 2)
        if self.qk.get(here) == 'K' and any(v == 15 for v in s.visible().values()):
            r = self.fight()
            if r is not None: return
        # tanken?
        if s.bar() <= self.refuel and self.bases:
            bq = self.bases
            known_b = {c for c, v in self.known.items() if v == 8}
            if known_b:
                p = self.plan(lambda c: c in known_b, through_goal=True)
            else:
                p = self.plan(lambda c: (c[0] >> 2, c[1] >> 2) in bq)
            if p:
                return self.go(p)
        # Sensor?
        if self.sensor_mode == 'dir':
            best = None
            for d in (6, 9, 0xA, 8):
                dx, dy = DIRS[d]
                unk = [q for q in (((here[0] + dx) & 3, (here[1] + dy) & 3), ((here[0] - dx) & 3, (here[1] - dy) & 3)) if q not in self.qk]
                if best is None or len(unk) > best[0]: best = (len(unk), d)
            if best[0] == 2 and s.bar() >= 3:
                self.stats['sensor'] += 1
                return s.sensor(best[1])
        elif self.sensor_mode != 'none':
            row = here[1]
            unknown = [((here[0] + dq) & 3, row) for dq in (-1, 1) if ((here[0] + dq) & 3, row) not in self.qk]
            if unknown and (self.sensor_mode == 'always' or row not in self.scanned_rows) and s.bar() >= 3:
                self.scanned_rows.add(row)
                self.stats['sensor'] += 1
                return s.sensor()
        # naechster Quadrant: wenig Energie und keine Basis bekannt -> Basis suchen; sonst Klingone
        tg = []
        if s.bar() <= self.bsearch and not self.bases:
            tg = [(qx, qy) for qx in range(4) for qy in range(4) if (qx, qy) not in self.bseen and self.qk.get((qx, qy)) != 'K']
            if not tg: tg = [(qx, qy) for qx in range(4) for qy in range(4) if (qx, qy) not in self.bseen]
        if not tg:
            tg = [q for q, v in self.qk.items() if v == 'K' and q != here]
        if not tg:
            tg = [(qx, qy) for qx in range(4) for qy in range(4) if (qx, qy) not in self.qk]
        if not tg:
            tg = [(qx, qy) for qx in range(4) for qy in range(4) if self.qk.get((qx, qy)) == 'K']
        tgs = set(tg)
        p = self.plan(lambda c: (c[0] >> 2, c[1] >> 2) in tgs)
        if not p:
            # festgefahren: zufaellig ziehen
            d = random.choice(list(DIRS)); return self.go([(d, 1)])
        return self.go(p)

    def _end(self, m):
        d, n = m; dx, dy = DIRS[d]
        return (self.s.x + n * dx) & 15, (self.s.y + n * dy) & 15


def random_player(sim, rng):
    while not sim.result:
        r = rng.random()
        if r < 0.15: sim.sensor(rng.choice(list(DIRS)))
        elif r < 0.4: sim.phaser(rng.choice(list(DIRS)), rng.randrange(1, 4))
        elif r < 0.85: sim.nav(rng.choice(list(DIRS)), rng.randrange(1, 8))
        else: sim.torp()


def play(D, E, seed, dmax=15, tlimit=52, tmax=1, bases=1, navcost=4, senscost=32, sensbase=True, phcost='l16', emax=255, **kw):
    rng = random.Random(seed)
    random.seed(seed)
    s = Sim(D, E, rng, dmg=lambda: 2 * rng.randrange(dmax + 1), tlimit=tlimit, tmax=tmax, bases=bases, navcost=navcost, senscost=senscost, sensbase=sensbase, phcost=phcost, emax=emax)
    if kw.get('rand'):
        random_player(s, rng)
        return s, None
    p = Player(s, **kw)
    guard = 0
    while not s.result:
        t0 = (s.t, s.energy, s.x, s.y, s.torps, s.N, s.sens is not None)
        p.step()
        if (s.t, s.energy, s.x, s.y, s.torps, s.N, s.sens is not None) == t0:
            guard += 1
            if guard > 20:
                s.result = 'haengt'; break
        else:
            guard = 0
    return s, p
