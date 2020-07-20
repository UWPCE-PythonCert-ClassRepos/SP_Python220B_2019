# pylint: disable=invalid-name
"""Read file and parse for info"""
import csv
from collections import defaultdict


def analyze(filename):
    """
    Analyze the given csv file:
        * count the number of rows for each year
        * count the number of rows with "ao"
    """

    # variables
    year_count = defaultdict(int)
    ao_count = 0

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            # parse the year
            # (using a substring to get the year is brittle but fast)
            year = row[5][6:]
            year_count[year] += 1

            # parse for ao
            if row[6] == "ao":
                ao_count += 1

    # print info
    print(dict(year_count))
    print(f"'ao' was found {ao_count} times")


if __name__ == "__main__":
    analyze("data/exercise.csv")
