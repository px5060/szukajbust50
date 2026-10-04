"""Zgodność silnika z appką T50 RAZEM: 8 modeli 1T (zakłady, cykle, WIN, BUST, bilans) vs wzorzec z t50x1x.html.
Uruchom:  python3 check.py [ścieżka do all50/src/apps/t50x1x.html]   (domyślnie ../../all50/src/apps/t50x1x.html)"""
import re, sys, pathlib, numpy as np
from engine import *
HERE = pathlib.Path(__file__).resolve().parent
app = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent.parent / 'all50' / 'src' / 'apps' / 't50x1x.html')
s = app.read_text()
seed = re.sub(r'\D', '', (HERE / 'seed_t50.txt').read_text())
codes = [seed[i:i + 3] for i in range(0, len(seed), 3)]
al = ALPH['t50']; X = np.array([al.index(c) for c in codes]); y = np.array([c[1] == '1' for c in al], np.uint8)
mods = re.findall(r"\{ id: '([^']+)',\s*typ: '[^']+', STEP: '([^']+)',\s*xSTEP: (\d), TRIGGER: '([^']+)',\s*offset: (\d) \}", s)
exp = dict((k, v) for k, v in re.findall(r"'([0-9A-Z_]+)':\s*\[([^\]]+)\]", s))
out = np.zeros(11, np.int64); bad = 0
for mid, S, x, T, o in mods:
    a, la = table(S, al); b, lb = table(T, al)
    sim(a, la, b, lb, int(x), int(o), X, y, len(X), out)
    e = [float(v) for v in exp[mid].split(',')]
    got = (out[0], out[1] + out[2], out[1], out[2], out[3])
    ok = got == (e[0], e[1], e[2], e[3], e[5]); bad += not ok
    print(mid, 'zakł/cykle/W/B/bilans', tuple(int(v) for v in got), 'OK' if ok else f'RÓŻNICA (wzorzec {e[:4]}, {e[5]})')
print('modeli:', len(mods), 'różnic:', bad)
