"""
Good performing, better written module
"""

import datetime
import csv


def analyze(filename):
    """Analyzes file for certain years and letters"""
    start = datetime.datetime.now()
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
        found = 0
        for row in reader:
            year = row[5][6:]
            if year in year_count:
                year_count[year] += 1
            if 'ao' in row[6]:
                found += 1
        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return start, end, year_count, found


def main():
    """

    :return:None
    """
    filename = "exercise2.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
