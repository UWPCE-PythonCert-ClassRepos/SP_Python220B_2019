#! /usr/bin/env python3

"""
well performing, well written module

"""
from collections import OrderedDict
import datetime
import csv


def analyze(filename):
    """ This function analyzes a data file """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        found = 0
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = {}
        for row in reader:
            if row[5] > '00/00/2012':
                try:
                    year_count[row[5][6:]] += 1
                except KeyError:
                    year_count[row[5][6:]] = 1

            if "ao" in row[6]:
                found += 1

        print(dict(OrderedDict(sorted(year_count.items(),
                                      key=lambda t: t[0]))))
        print(f"'ao' was found {found} times")

    end = datetime.datetime.now()
    return (start, end, year_count, found)


def main():
    """ The main entry point function """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
