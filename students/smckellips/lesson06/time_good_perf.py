# pylint: disable=W0611
'''Timing wrapper'''
from timeit import timeit
from good_perf import main #main,analyze
from poor_perf import main as poor_main

REPS = 5
FILE = "data/exercise.csv"

# time = timeit('analyze(FILE)', number=REPS, globals=globals())
TIME = timeit('main()', number=REPS, globals=globals())
print(f'Average time = {TIME/REPS:.2f}s')

TIME2 = timeit('poor_main()', number=REPS, globals=globals())
print(f'Average time = {TIME2/REPS:.2f}s')
