"""
evidence-based testing of poorly performing, well written module
"""

#from timeit import timeit as timer

import datetime
import csv


def analyze(filename):
    """returns the count of entries with a year between 2013 and 2018; compiles count of all
       entries with 'ao' in the final column of the input file"""

    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        found = 0
        for row in reader:
            if row[6] == "ao":
                found += 1
            try:
                year_count[row[5][6:]] += 1
            except KeyError:
                pass

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


if __name__ == "__main__":
    INPUT = "data/exercise.csv"
    analyze(INPUT)
