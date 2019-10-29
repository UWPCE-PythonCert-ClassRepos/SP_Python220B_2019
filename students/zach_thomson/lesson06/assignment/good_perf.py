"""
better performing, better written module
"""

import datetime
import csv


def analyze(filename):
    '''main analysis function'''
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
            lrow = list(row)
            if '2019' > lrow[5][6:] > '2012':
                year_count[lrow[5][6:]] += 1
            if lrow[6] == 'ao':
                found += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    '''main function that finds data file and runs analyze func'''
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
