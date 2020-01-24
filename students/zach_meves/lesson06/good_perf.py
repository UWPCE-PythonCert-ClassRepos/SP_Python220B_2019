"""
Better performing code.
"""

import datetime
import csv
import logging

# Attempt to use Cython version
try:
    import good_perf_cython
except ImportError:
    pass


def analyze(filename):
    """Analyze the file."""

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
            year = row[5][-4:]
            if year in year_count:
                year_count[year] += 1

            if 'ao' in row[6]:
                found += 1

        # Re-create the 'bug' found in poor_perf.py
        year_count['2017'] += year_count['2018']
        year_count['2018'] = 0

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    """Analyze file."""
    filename = "data/exercise.csv"
    try:
        good_perf_cython.analyze(filename)
        logging.info("Using Cython version of code")
    except NameError:
        logging.info("Using non-Cython version of code")
        analyze(filename)


if __name__ == "__main__":
    main()
