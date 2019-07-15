"""
Hopefully a better performing version compared to poor_perf.py
"""

import datetime
import csv
import time

def analyze(filename):
    """
    Return how many rows contained years 2013-2018
    and how many times 'ao' was found
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

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
            year = row[5][6:]
            if year in year_count:
                year_count[year] += 1
            if "ao" in row[6]:
                found += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


def main():
    """
    Main
    """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    START_TIME = time.time()
    main()
    print("{} seconds".format(time.time() - START_TIME))
