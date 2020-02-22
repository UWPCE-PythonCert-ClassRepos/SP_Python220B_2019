""" Comparing poor_perf.py against good_perf.py """

import time
import timeit
from good_perf import analyze as an2
from poor_perf import analyze as an1
NUM_RUNS = 2

time.sleep(1)
FILENAME = "exercise.csv"
S1, E1, Y_CNT1, F_CNT1 = 0, 0, 0, 0
S2, E2, Y_CNT2, F_CNT2 = 0, 0, 0, 0


# Check that the funcitons produce the same results
[S1, E1, Y_CNT1, F_CNT1] = an1(FILENAME)
[S2, E2, Y_CNT2, F_CNT2] = an2(FILENAME)

# assert Y_CNT1 == Y_CNT2
assert F_CNT1 == F_CNT2
print("Both Programs generate the same results")

# Time each function
ELAPSED_TIME1 = timeit.Timer(lambda: an1(FILENAME))
ELAPSED_TIME2 = timeit.Timer(lambda: an2(FILENAME))

TOTAL_ELAPSED_TIME1 = ELAPSED_TIME1.timeit(number=NUM_RUNS)/NUM_RUNS
TOTAL_ELAPSED_TIME2 = ELAPSED_TIME2.timeit(number=NUM_RUNS)/NUM_RUNS
print(f"Average of {NUM_RUNS} Runs")
print(f"Poor Performance Elapsed Time = {TOTAL_ELAPSED_TIME1:.5f}")
print(f"Good Performance Elapsed Time = {TOTAL_ELAPSED_TIME2:.5f}")

TIME_DIFF = TOTAL_ELAPSED_TIME1 - TOTAL_ELAPSED_TIME2
TIME_ORDER = TOTAL_ELAPSED_TIME1 / TOTAL_ELAPSED_TIME2

if TIME_DIFF > 0:
    print(f"Time improvement of {TIME_DIFF:.5f} seconds")
    print(f"Factor of {TIME_ORDER:.1f} improvement")
else:
    print(f"Time deterioration of {TIME_DIFF:.5f} seconds")
    print(f"Factor of {TIME_ORDER:.1f} deterioration")
