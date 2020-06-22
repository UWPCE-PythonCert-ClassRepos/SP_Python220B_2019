"""
Good performing module
"""

import datetime
import csv
from statistics import mean
from timeit import repeat

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        for row in reader:
            if row[5][6:] in year_count.keys():
                year_count[row[5][6:]] += 1
            if "ao" in row[6]:
                found += 1
        print(year_count)
        print(f" 'ao' was found {found} times")
        end = datetime.datetime.now
    return(start, end, year_count, found)

def main():
# add in same avg of times/reps as in poor_perf.py
    repitions = 5
    testing = '''filename = "exercise.csv"
analyze(filename)'''
    timer = repeat(stmt=testing, globals=globals(), repeat=repitions, number=1)
    print('the avg of ' + str(repitions) + 'runs of the good_perf module timeit is:')
    print(mean(timer))

if __name__ == "__main__":
    main()
