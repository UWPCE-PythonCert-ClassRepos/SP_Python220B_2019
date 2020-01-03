# Advanced Programming In Python - Lesson 6 Assignment 1: Performance
# RedMine Issue - SchoolOps-16
# Code Poet: Anthony McKeever
# Start Date: 01/01/2019
# End Date: 01/02/2019

"""
Analyze a file for records between 2013 and 2018 and
the number of occurances of "ao".
"""

import csv
from datetime import datetime


def analyze(filename):
    """
    Analyzes the desired file.

    :filename:  The name and path to the file.
    """
    start = datetime.now()
    ao_count = 0
    year_count = {"2013": 0,
                  "2014": 0,
                  "2015": 0,
                  "2016": 0,
                  "2017": 0,
                  "2018": 0}

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for row in reader:
            ao_count += 1 if row[-1] == "ao" else 0
            year = row[-2][-4:]

            if year in year_count.keys():
                year_count[year] += 1

    print(year_count)
    print(f"'ao' was found {ao_count} times")

    end = datetime.now()
    return (start, end, year_count, ao_count)


def main():
    """ The main application method """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
