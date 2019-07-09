"""
poorly performing, poorly written module

"""

import datetime
import csv
import timeit
from collections import defaultdict

FILE_NAME = "data/exercise_file.csv"


def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count_dict = defaultdict(int)

        found = 0
        for row in reader:

            if 2019 > int(row[5][6:]) > 2012:
                year_count_dict[row[5][6:]] += 1

            if "ao" in row:
                found += 1

        print(f"'ao' was found {found} times")

        #print(sorted(year_count_dict))
        print(dict(sorted(year_count_dict.items())))

        end = datetime.datetime.now()

    return (start, end, year_count_dict, found)


def main():

    print(timeit.timeit("analyze(FILE_NAME)",
                        setup="from __main__ import analyze, FILE_NAME", 
                        number=1))


if __name__ == "__main__":
    main()