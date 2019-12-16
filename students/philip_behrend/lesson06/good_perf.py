"""
Improved module to import and analyze data
"""

import datetime
import csv

def analyze(filename):
    """ Analyzes input file, outputs performance metrics and count data """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # new_ones = []
        found = 0
        year_count = {
            "2010": 0,
            "2011": 0,
            "2012": 0,
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0,
            "2019": 0
        }
        for row in reader:
            lrow = list(row)
            if lrow[6] == 'ao':
                found += 1
            yr_extract = lrow[5][6:]
            year_count[yr_extract] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


if __name__ == "__main__":
    strt, ending, yr_count, fnd = analyze("exercise_out.csv")
    print(f'Elapsed time: {(ending-strt).total_seconds()} seconds')
    print(yr_count, fnd)
