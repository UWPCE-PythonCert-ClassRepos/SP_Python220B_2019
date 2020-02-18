# Advanced Programming in Python -- Lesson 4 Exercise 2
# Jason Virtue
# Start Date 2/17/2020


def y_range(start, stop, step=1):
    i = start
    while i < stop:
        yield i
        i += step

print(y_range(1,10))