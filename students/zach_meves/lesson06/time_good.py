"""
Timer for ``good_perf.py``.
"""

import os
import good_perf
import cProfile
import pstats
import logging
from timeit import timeit

logging.basicConfig(level=logging.INFO)
NUMBER = 5

time = timeit("good_perf.main()", number=NUMBER, globals=globals())
print(f"Average time = {time/NUMBER:.2f}s")

print("Profile results:\n")
cProfile.runctx("good_perf.main()", globals(), locals(), filename='stats.o')
res = pstats.Stats('stats.o')
res.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats()

os.remove('stats.o')