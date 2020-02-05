"""
Better writting, better performing module

"""

import datetime
import csv
import timeit


def analyze(filename):
    """Print year counts, oa count and return start, end and both counts."""
    start = datetime.datetime.now()
    found = 0
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

        for row in reader:
            if "ao" in row[6]:
                found += 1
            if row[5][6:] in year_count:
                year_count[row[5][6:]] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """Main function changed to support timeit."""
    print(timeit.timeit("analyze('data/exercise.csv')",
                        setup='from __main__ import analyze', number=1))


if __name__ == "__main__":
    main()
