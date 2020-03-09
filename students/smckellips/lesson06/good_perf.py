"""
Better performing module.
"""

import datetime
import csv

def analyze(filename):
    '''Analyze data function refactored.'''
    start = datetime.datetime.now()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0
        for row in reader:
            if "ao" in row[6]:
                found += 1

            # if row[5][6:] < '2013':
            #     continue
            # if '2012' < row[5][6:]: # < '2019':
            if row[5][6:] > '2012':
                year_count[row[5][6:]] += 1

    print(year_count)

    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    '''Main module launch function'''
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
    # filename = "data/exercise.csv"
    # analyze(filename)
