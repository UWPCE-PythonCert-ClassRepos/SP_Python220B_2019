from timeit impor timeit as timer
repititions = 10000
my_range = 10000
lower_limit = my_range/2

my_list = list(range(my_range))

def multiple_by_two(x):
    return x * 2

def greater_than_lower_limit(x):
    return x > lower_limit

print (timer())


