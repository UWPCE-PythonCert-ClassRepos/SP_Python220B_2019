"""
Profiling video example code.
"""

from timeit import timeit as timer

reps = 10000
my_range = 10000
lower_limit = my_range / 2

my_list = list(range(my_range))

def multiply_by_two(x):
    return x * 2

def greater_than_lower_limit(x):
    return x > lower_limit

print('\n\nmap_filter_with_functions')
print(timer(
    'map_filter_with_functions = map(multiply_by_two, filter(greater_than_lower_limit, my_list))',
    #print(*map_filter_with_functions)
    globals=globals(),
    number=reps))

print('\n\nmap_filter_with_lambdas')
print(timer(
    'map_filter_with_lambdas = map(lambda x: x * 2, filter(lambda x: x > lower_limit, my_list))',
    #print(*map_filter_with_lambdas)
    globals=globals(),
    number=reps))

print('\n\ncomphrehension')
print(timer(
    'comprehension = [x * 2 for x in my_list if x > lower_limit]',
    #print(*comprehension)
    globals=globals(),
    number=reps))

print('\n\ncomphrehension_func')
print(timer(
    'comprehension_func = [multiply_by_two(x) for x in my_list if greater_than_lower_limit(x)]',
    #print(*comprehension_func)
    globals=globals(),
    number=reps))

print('\n\nlambda_comp')
print(timer(
    'lambda_comp = [(lambda x: x * 2)(x) for x in my_list if (lambda x: x > lower_limit)(x)]',
    #print(*lambda_comp)
    globals=globals(),
    number=reps))

# Guesses for timer
# 1. map_filter_with_functions
# 2. map_with_lambda
# 3. comprehension
# 4. comprehension function
# 5. lambda comp




