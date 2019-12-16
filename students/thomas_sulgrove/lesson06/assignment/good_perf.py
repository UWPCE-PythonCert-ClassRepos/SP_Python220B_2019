"""
better performing, better written module
"""

import datetime
import csv
import os


def analyze(filename):
    """counts the years found in the csv"""
    start = datetime.datetime.now()
    found = 0
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    year_count_keys = list(year_count.keys())
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[6] == 'ao':
                found += 1
            year = row[5][-4:]
            if year in year_count_keys:
                year_count[str(year)] += 1

        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """runs the thing."""
    filename = os.getcwd() + '\\data\exercise.csv'
    analyze(filename)


if __name__ == "__main__":
    main()
