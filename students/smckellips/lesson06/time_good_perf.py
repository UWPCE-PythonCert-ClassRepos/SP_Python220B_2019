from timeit import timeit
from good_perf import main,analyze

REPS = 25
FILE = "data/exercise.csv"

# time = timeit('analyze(FILE)', number=REPS, globals=globals())
time = timeit('main()', number=REPS, globals=globals())
print(f'Average time = {time/REPS:.2f}s')
