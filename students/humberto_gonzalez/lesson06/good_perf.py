"""
good performing, well written module

"""
# pylint: disable=duplicate-code

import datetime
import csv

def analyze(filename):
    """Analyzes the data files"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        year_count = {"2013": 0,
                      "2014": 0,
                      "2015": 0,
                      "2016": 0,
                      "2017": 0,
                      "2018": 0}

        found = 0

        for row in reader:
            date = row[5]
            ending = row[6]

            if date[6:] == '2013':
                year_count["2013"] += 1
            if date[6:] == '2014':
                year_count["2014"] += 1
            if date[6:] == '2015':
                year_count["2015"] += 1
            if date[6:] == '2016':
                year_count["2016"] += 1
            if date[6:] == '2017':
                year_count["2017"] += 1
            if date[6:] == '2018':
                year_count["2017"] += 1
            if "ao" in ending:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """runs the main function"""
    filename = "./data/randomdata.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
