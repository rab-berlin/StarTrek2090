# sim_m2.py - schnelles Regelmodell von startrek-m02 (1 Basis, 1 Torpedo, Energie 255, Zeit nach 51 Aktionen; gegen den Emulator geprueft: sim_check.py)
import random


def rotl(v):
    return ((v << 1) | (v >> 3)) & 0xF


class Ref:
    """Referenzmodell der Galaxie aus M0-M5."""
    ONE_BASE = False      # True: eine Basis im Quadranten Q = sB (startrek-m02 ab der Variante mit 1 Basis)

    def __init__(self, M):
        self.rows = M[0:4]
        self.sK, self.sB = M[4], M[5]

    def quad(self, qx, qy):
        Q = qy * 4 + qx
        kal = (self.rows[qy] >> qx) & 1
        base = (Q == self.sB) if self.ONE_BASE else ((Q + self.sB) & 7) == 0
        ks = rotl((Q + self.sK) & 0xF)
        bs = (ks + 8) & 0xF if base else ks
        s1 = rotl((ks + self.sB) & 0xF)
        s2 = (s1 + ks) & 0xF
        return dict(kal=kal, base=base, ks=ks, bs=bs, s1=s1, s2=s2)

    def cell(self, x, y):
        q = self.quad(x >> 2, y >> 2)
        s = (y & 3) * 4 + (x & 3)
        if s == q['ks'] and q['kal']:
            return 0xF
        if s == q['bs'] and q['base']:
            return 8
        if s in (q['s1'], q['s2']):
            return 1
        return 0


DIRS = {0: (-1, -1), 1: (0, -1), 2: (1, -1), 4: (-1, 0), 6: (1, 0), 8: (-1, 1), 9: (0, 1), 0xA: (1, 1)}
VEC = {v: k for k, v in DIRS.items()}


class Sim:
    """Ein Spiel. Galaxie aus D = RD, E = RE beim RUN; Schaden 2 * (0..15)."""

    def __init__(self, D, E, rng, dmg=None, tlimit=52, tmax=1, bases=1, navcost=4, senscost=32, sensbase=True, phcost='l16', emax=255):
        self.tlimit, self.tmax, self.bases, self.navcost, self.senscost = tlimit, tmax, bases, navcost, senscost
        self.ref = Ref([D, E, D ^ 15, E ^ 15, D, E] + [0] * 10)
        self.ref.ONE_BASE = (bases == 1)
        self.phmode = phcost        # Phaserkosten: l16 = 16 je Stufe, f16/f32 = fest, l1 = 1 je Stufe, l8 = 8 je Stufe
        self.sensbase = sensbase      # Sensor zeigt die Basis auch neben einem Klingonen (eigene Farbe)
        self.rng = rng
        self.dmg = dmg or (lambda: 2 * rng.randrange(16))
        self.x = self.y = 0
        self.emax = emax            # 255: Balken je 32 (Energie / 32 + 1 Pixel); 200: je 25
        self.energy, self.torps, self.N, self.t = emax, tmax, 8, 0
        self.result = None          # 'win', 'energie', 'zeit'
        self.sens = None
        self.actions = 0
        self.log = []
        self._tick()

    # --- Hilfen
    def cell(self, x, y):
        return self.ref.cell(x & 15, y & 15)

    def kal_here(self):
        return self.ref.quad(self.x >> 2, self.y >> 2)['kal']

    def _kill(self, x, y):
        self.ref.rows[(y >> 2) & 3] &= ~(1 << ((x >> 2) & 3)) & 15
        self.N -= 1
        if self.N == 0:
            self.result = 'win'

    def _tick(self):
        self.t += 1
        if self.t >= self.tlimit:
            self.result = 'zeit'; return
        if self.kal_here():
            d = self.dmg()
            self.energy -= d
            self.log.append(('feuer', d))
            if self.energy < 0:
                self.result = 'energie'

    # --- Befehle (geben True zurueck, wenn eine Aktion stattfand)
    def nav(self, d, n):
        if n == 0 or self.result: return False
        self.sens = None
        dx, dy = DIRS[d]
        for _ in range(n):
            cx, cy = (self.x + dx) & 15, (self.y + dy) & 15
            c = self.cell(cx, cy)
            if c:
                if c == 8:
                    self.energy, self.torps = self.emax, self.tmax
                    self.log.append(('andocken',))
                break
            self.x, self.y = cx, cy
            self.energy -= self.navcost
            if self.energy < 0:
                self.result = 'energie'; return True
        self.actions += 1
        self._tick()
        return True

    def sensor(self):
        if self.result: return False
        self.energy -= self.senscost
        if self.energy < 0:
            self.result = 'energie'; return True
        qx, qy = self.x >> 2, self.y >> 2
        out = {}
        for dq in (-1, 1):
            q = self.ref.quad((qx + dq) & 3, qy)
            out[(qx + dq) & 3, qy] = ('KB' if self.sensbase and q['base'] else 'K') if q['kal'] else ('B' if q['base'] else '-')
        self.actions += 1
        self._tick()
        self.sens = out
        return True

    def phaser(self, d, k):
        if k == 0 or self.result: return False
        self.sens = None
        self.energy -= self.phcost(k)
        if self.energy < 0:
            self.result = 'energie'; return True
        dx, dy = DIRS[d]
        cx, cy, code = self.x, self.y, 0
        for _ in range(k):
            cx, cy = (cx + dx) & 15, (cy + dy) & 15
            code = self.cell(cx, cy)
            if code: break
        self.actions += 1
        if code == 15:
            self._kill(cx, cy)
            if self.result: return True
        self._tick()
        return True

    def torp(self):
        if self.result or self.torps == 0 or not self.kal_here(): return False
        self.sens = None
        self.torps -= 1
        self.actions += 1
        self._kill(self.x, self.y)
        if not self.result: self._tick()
        return True

    def phcost(self, k):
        return {'l16': 16 * k, 'f16': 16, 'f32': 32, 'l1': k, 'l8': 8 * k, 'f0': 0}[self.phmode]

    # --- was der Spieler sieht
    def bar(self):
        if self.emax == 255: return max(0, min(self.energy // 32 + 1, 8))
        return max(0, min(self.energy // 25, 8))

    def bar_low(self):
        """untere Grenze der Energie, die der Balken verraet"""
        b = self.bar()
        return 32 * (b - 1) if self.emax == 255 else 25 * b

    def visible(self):
        """Inhalt des eigenen Quadranten (absolute Koordinaten -> Code)."""
        qx, qy = self.x >> 2, self.y >> 2
        return {(4 * qx + i, 4 * qy + j): self.cell(4 * qx + i, 4 * qy + j) for i in range(4) for j in range(4)}
