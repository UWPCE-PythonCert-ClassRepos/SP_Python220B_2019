# pylint: disable=W0611
'''Timing wrapper'''
from timeit import timeit
from good_perf import main
from poor_perf import main as poor_main

REPS = 3

# time = timeit('analyze(FILE)', number=REPS, globals=globals())
TIME = timeit('main()', number=REPS, globals=globals())
print(f'Good Average time = {TIME/REPS:.2f}s')

TIME2 = timeit('poor_main()', number=REPS, globals=globals())
print(f'Poor Average time = {TIME2/REPS:.2f}s')


num_rows = 0
for row in open("data/exercise.csv"):
    num_rows += 1
print(f'Out of {num_rows} rows')


# C:\Users\v-ollock\github\SP_Python220B_2019\students\ScotchWSplenda\lesson06\assignment
# python -m pylint ./good_perf.py
# python -m pylint ./poor_perf.py
# python -m pylint ./create_data.py
# python -m pylint ./time_trial.py
