"""
Less poorly performing, less poorly written module

"""

from timeit import timeit as timer
import datetime
import csv

FILENAME = "data/exercise.csv"


def analyze(filename):
    """Analyzes the given file for year and ao counts"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        found = 0
        for row in reader:
            if "ao" in row[6]:
                found += 1
            if row[5] > '00/00/2012':
                new_ones.append((row[5], row[0]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:

            year_check = new[0][6:]

            if year_check in year_count:
                year_count[year_check] += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    """Runs the analyze function and times it"""
    print(timer("analyze(filename)", setup="from __main__ import analyze, filename", number=5))


if __name__ == "__main__":
    main()
