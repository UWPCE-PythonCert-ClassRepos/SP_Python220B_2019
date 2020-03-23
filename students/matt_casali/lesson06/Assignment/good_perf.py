#!/usr/bin/env python3

"""
Good performance module

"""

# pylint: disable= C0103

import datetime
import csv
import time


def analyze(filename):
    """
    This function will take a csv file as an input and return the year count and ao count
    within the file
    :param filename: CSV file path.
    :return: A dictionary showing the year count and a print statement of the ao count.
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
            year_count[row[5][6:]] += 1
            if "ao" in row[6]:
                found += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    """
    This is the main function that calls the analyze function.
    :return:
    """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("{}".format(time.time() - start_time))
