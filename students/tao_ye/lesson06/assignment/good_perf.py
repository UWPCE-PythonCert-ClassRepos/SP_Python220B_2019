"""
improved performance module
"""

import datetime
import csv

import time


def analyze(filename):
    """ analyze data in a csv file """
    start = datetime.datetime.now()

    time_start = time.perf_counter()

    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    found = 0

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in reader:
            if "ao" in row[6]:
                found += 1

            if row[5][6:] == '2013':
                year_count["2013"] += 1
                continue
            if row[5][6:] == '2014':
                year_count["2014"] += 1
                continue
            if row[5][6:] == '2015':
                year_count["2015"] += 1
                continue
            if row[5][6:] == '2016':
                year_count["2016"] += 1
                continue
            if row[5][6:] == '2017':
                year_count["2017"] += 1
                continue
            if row[5][6:] == '2018':
                year_count["2018"] += 1
                continue

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    time_stop = time.perf_counter()

    print(f'Total Process time: {(time_stop-time_start):12.6f}')

    return (start, end, year_count, found)


def main():
    """ program main """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
