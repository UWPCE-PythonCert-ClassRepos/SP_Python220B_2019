"""
Eliminated if statements for the year_count.
"""

import datetime
import csv
import time

def analyze(filename):
    """Count instances of each year and 'ao' in a csv file."""

    start = time.time()
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

        ao_count = 0

        for row in reader:
            year_count[row[5][-4:]] += 1

            if 'ao' in row[6]:
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
