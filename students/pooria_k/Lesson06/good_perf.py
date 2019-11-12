"""
poorly performing, poorly written module

"""

import datetime
import csv

def analyze(filename):
    """Read CSV file line by line
        Analyzie it, create year_count and count how manytimes
        'ao' was found
    """
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    found = 0
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            date = row[5][6:]
            if date in year_count:
                year_count[date] += 1
            if "ao" in row[6]:
                found += 1
        print(year_count)
        print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return start, end, year_count, found

def main():
    """main function to set filename
    and call analyze function"""
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
