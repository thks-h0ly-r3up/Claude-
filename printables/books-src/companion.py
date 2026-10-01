from companion_days_1 import DAYS_1
from companion_days_2 import DAYS_2
from companion_days_3 import DAYS_3
COMPANION_DAYS = DAYS_1 + DAYS_2 + DAYS_3
assert [d[0] for d in COMPANION_DAYS] == list(range(1, 91))
