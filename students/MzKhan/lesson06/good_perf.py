"""
Improved performance of poor_perf.py
"""

import datetime
import csv

def analyze(filename):
    "return the number of years occurances and the count of ao"
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
            lrow = list(row)
            found = found + 1 if 'ao' in lrow[6] else found
            year = lrow[5][-4:]
            if year in year_count:
                year_count[year] += 1
        print(year_count)
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return (start, end, year_count, found)


if __name__ == "__main__":
    FILE_NAME = "data/exercise.csv"
    analyze(FILE_NAME)
