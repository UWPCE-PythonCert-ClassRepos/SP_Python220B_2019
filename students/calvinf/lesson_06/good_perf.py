"""
poorly performing, poorly written module

"""

import datetime
import csv


def analyze(filename):
    """Function to read the contents of a csv and produce statistic on contents"""
    start = datetime.datetime.now()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        for row in reader:
            lrow = list(row)
            place = lrow[5][6:]
            if "ao" in lrow[6]:
                found += 1
            if place == '2013':
                year_count["2013"] += 1
            if place == '2014':
                year_count["2014"] += 1
            if place == '2015':
                year_count["2015"] += 1
            if place == '2016':
                year_count["2016"] += 1
            if place == '2017':
                year_count["2017"] += 1
            if place == '2018':
                year_count["2017"] += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
    return start, end, year_count, found


def main():
    """Main function to module"""
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
