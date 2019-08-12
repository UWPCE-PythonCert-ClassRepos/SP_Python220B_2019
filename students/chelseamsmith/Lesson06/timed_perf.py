"""
poorly performing, poorly written module

"""

import datetime
import csv
from timeit import timeit as timer

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            lrow = list(row)
            if "ao" in row[6]:
                found += 1

            if lrow[5][-4:] == '2013':
                year_count["2013"] += 1
            elif lrow[5][-4:] == '2014':
                year_count["2014"] += 1
            elif lrow[5][-4:] == '2015':
                year_count["2015"] += 1
            elif lrow[5][-4:] == '2016':
                year_count["2016"] += 1
            elif lrow[5][-4:] == '2017':
                year_count["2017"] += 1
            elif lrow[5][-4:] == '2018':
                year_count["2017"] += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
