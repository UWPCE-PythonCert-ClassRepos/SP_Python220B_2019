#!/usr/bin/env python3

# Russell Felts
# Assignment 6

""" Improved performance module """

import datetime
import csv


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
            lrow = list(row)
            # Update year count based on the year in the row
            if lrow[5][-4:] in year_count:
                year_count[lrow[5][-4:]] += 1
            # Add 1 to the ao found count
            if "ao" in lrow[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    """
    Main function
    """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
