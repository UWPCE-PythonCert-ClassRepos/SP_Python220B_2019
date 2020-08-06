# Stella Kim
# Assignment 6: Finding Bottlenecks

"""Updated module to run code in a more efficient and timely manner"""

import datetime
import csv
from timeit import timeit as timer


def analyze(filename):
    """Analyze CSV data and tally 'ao' and year count entries"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        year_count = {
            '2013': 0,
            '2014': 0,
            '2015': 0,
            '2016': 0,
            '2017': 0,
            '2018': 0
        }

        for row in reader:
            if 'ao' in row[6]:
                found += 1

            year_key = row[5][-4:]
            if year_key in year_count:
                year_count[year_key] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


def _code_timer():
    """Measure time it takes to run function(s)"""
    print(timer("analyze('./data/data.csv')", globals=globals(), number=1))


if __name__ == "__main__":
    analyze('./data/data.csv')
    # _code_timer()
