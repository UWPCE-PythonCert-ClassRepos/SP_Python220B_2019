'''Timeit comparisions between'''

import timeit
import os

GOOD_FILE = os.getcwd() + '\\good_perf.py'
POOR_FILE = os.getcwd() + '\\poor_perf.py'

GOOD = timeit.timeit(stmt="subprocess.call(['python', r'{}'])".format(GOOD_FILE),
                     setup="import subprocess", number=5)

POOR = timeit.timeit(stmt="subprocess.call(['python', r'{}'])".format(POOR_FILE),
                     setup="import subprocess", number=5)
print("Poor: {0:.2f}, Good: {1:.2f}, Improvement: {2:.2f}x".format(POOR, GOOD, POOR / GOOD))
