"""Merge the rewritten (daughter-of-an-addicted-mother, cycle-breaking) text onto the verse/reading data."""
from companion_days_1 import DAYS_1
from companion_days_2 import DAYS_2
from companion_days_3 import DAYS_3
from standing_rewrite_1 import R1
from standing_rewrite_2 import R2
from standing_rewrite_3 import R3

_OLD = DAYS_1 + DAYS_2 + DAYS_3
_NEW = {**R1, **R2, **R3}
assert sorted(_NEW) == list(range(1, 91)), sorted(set(range(1, 91)) - set(_NEW))

COMPANION_DAYS = []
for (n, _t, _l, vref, vq, _te, _a, _ac, _p, _d, also) in _OLD:
    r = _NEW[n]
    title, lens, teach, asks, act, pray, decl = r[:7]
    if len(r) > 7:
        vref, vq = r[7]
    COMPANION_DAYS.append((n, title, lens, vref, vq, teach, asks, act, pray, decl, also))
assert [d[0] for d in COMPANION_DAYS] == list(range(1, 91))
