# pylint: disable=W0611
'''Timing wrapper'''
from timeit import timeit
from linear import import_data, reset_db

REPS = 1
# FILE = "data/exercise.csv"

# time = timeit('analyze(FILE)', number=REPS, globals=globals())

        # count, errors = import_data(
        #     'data', 'products.csv', 'customers.csv', 'rentals.csv')
def time_linear():
    ''' Repeatable function for timing '''
    reset_db()
    import_data("data", "products.csv", "customers.csv", "rentals.csv")

TIME = timeit('time_linear()', number=REPS, globals=globals())
print(f'Average time = {TIME/REPS:.2f}s')

# TIME2 = timeit('async_import()', number=REPS, globals=globals())
# print(f'Average time = {TIME2/REPS:.2f}s')
