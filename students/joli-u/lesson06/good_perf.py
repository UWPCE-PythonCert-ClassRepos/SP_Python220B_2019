"""
good_perf.py
Joli Umetsu
Assignment 6
PY220
"""

import csv
from timeit import timeit

def analyze(filename):
    year_count = {"2013": 0,
                  "2014": 0,
                  "2015": 0,
                  "2016": 0,
                  "2017": 0,
                  "2018": 0}

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        for row in reader:
            if "ao" in row[6]:
                found += 1
            if row[5][6:] in year_count:
                year_count[row[5][6:]] += 1

        print(year_count)
        print(f"'ao' was found {found} times")

    return (year_count, found)

def main():
    print(timeit('analyze("data/exercise.csv")', globals=globals(), number=3), "seconds (3 runs)")


if __name__ == "__main__":
    main()
