"""
Updated, higher performance module.
"""

import datetime
import csv

def analyze(filename):
    """Analyzes .csv filename for count of years in date and count of a string appearance"""
    start = datetime.datetime.now()
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
            if '2012' < row[5][6:] < '2019':
                year_count[row[5][6:]] += 1
            if "ao" in row[6]:
                found += 1

        print(year_count)
        print("'ao' was found {} times".format(found))
        end = datetime.datetime.now()

    return start, end, year_count, found

def main():
    """Main module function."""
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
