"""Module for improving performance of poor_perf.py"""

import datetime
import csv


def analyze(filename):
    """Return year of occurrencesa and count for ao"""
    start = datetime.datetime.now()  # Track start time
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        year_count = {"2013": 0,
                      "2014": 0,
                      "2015": 0,
                      "2016": 0,
                      "2017": 0,
                      "2018": 0}

        ao_count = 0
        for row in reader:
            if row[5][6:] == '2013':
                year_count["2013"] += 1
            if row[5][6:] == '2014':
                year_count["2014"] += 1
            if row[5][6:] == '2015':
                year_count["2015"] += 1
            if row[5][6:] == '2016':
                year_count["2016"] += 1
            if row[5][6:] == '2017':
                year_count["2017"] += 1
            if row[5][6:] == '2018':
                year_count["2018"] += 1
            if row[6] == "ao":
                ao_count += 1

        print(year_count)
        print(f"'ao' was found {ao_count} times")

        end = datetime.datetime.now()  # Track end time
    return (start, end, year_count, ao_count)


if __name__ == "__main__":
    FILE_NAME = "data/exercise.csv"
    analyze(FILE_NAME)
