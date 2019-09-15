#!/usr/bin/env python3

# Russell Felts
# Assignment 6

""" Poorly performing, poorly written timing module """

# pylint: disable=possibly-unused-variable

import csv
import datetime
from timeit import timeit as timer


def analyze(filename):
    """
    Read over a csv file and gather a count for the number of times a
    specific year and 'ao' is encountered
    :param filename: csv file to read
    :return: start date, end date, dictionary containing year count,
    and integer containing the number of times 'ao' was found
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        print(timer(
            """for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))""", globals=locals(), number=1),
              "seconds to append new dates to the list", )

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        print(timer(
            """for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1""", globals=locals(), number=1),
              "seconds to add up year counts", )

        # print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        print(timer(
            """found = 0
for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1""", globals=locals(), number=1),
              "seconds to count the number of ao's found", )

    # print(f"'ao' was found {found} times")
    # end = datetime.datetime.now()

    # return (start, end, year_count, found)


def main():
    """ Main function """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
