# Advanced Programming in Python -- Lesson 4 Exercise 1
# Jason Virtue
# Start Date 2/17/2020

"""
Simple iterator examples
"""

class IterateMe_1:
    """

    returns a sequence of numbers
    ( like range() )
    """

    def __init__(self, start, increment, stop):
        self.start = start
        self.increment = increment
        self.stop = stop
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        self.current += self.increment
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

if __name__ == "__main__":

    iter = IterateMe_1(5,2,17)
    for i in iter:
        if i >10: break
        print(i)
    # it's stateful
    for i in iter:
        print(i)

    # reinitialize "loses state"
    iter = IterateMe_1(5,2,17)
    for i in iter:
        print(i)