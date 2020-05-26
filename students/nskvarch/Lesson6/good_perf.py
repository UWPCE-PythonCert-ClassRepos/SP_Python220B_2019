"""
refactored module for Lesson 6 exercise Profiling and performance

"""

import datetime
import csv


def analyze(filename):
    """Return a count for certain years and if the "ao" tag was present"""
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

        for i in reader:
            year = i[5][6:]
            if year in year_count:
                year_count[year] += 1
            if "ao" in i[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
        # print(start, end)

    return start, end, year_count, found


def main():
    """Main program"""
    filename = r"data\exercise.csv"
    analyze(filename)


# Main program namespace
if __name__ == "__main__":
    main()
