"""
Combined the year and 'ao' checks.
"""

import datetime
import csv
import time

def analyze(filename):
    start = time.time()
    with open(filename) as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in rows:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[6]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        ao_count = 0

        for new in new_ones:
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
                year_count["2017"] += 1

            if 'ao' in new[1]:
                ao_count += 1

        print(year_count)
        print(f"'ao' was found {ao_count} times")

    print(f'{time.time() - start} seconds')

    return (year_count, ao_count)

def main():
    filename = "data/pre-panda_exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
