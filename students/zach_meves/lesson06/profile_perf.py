"""
Helper script to display profiling results.

Usage::
    > python profile_perf.py stats

``stats`` should be the output of a ``cProfile`` call, such
as::
    python -m cProfile -o stats module.py
"""

import sys
import pstats
from pstats import SortKey


if __name__ == "__main__":
    argv = sys.argv[1:]

    if not argv:
        print("Must supply a stats file to analyze.")
        sys.exit(1)

    p = pstats.Stats(argv[0])
    p.strip_dirs().sort_stats(SortKey.TIME).print_stats()
