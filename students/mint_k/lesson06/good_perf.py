"""
Lesson06

"""

import datetime
import csv


def analyze(filename):
    """this is to hash through the data"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        year_count = {
            "2010": 0,
            "2011": 0,
            "2012": 0,
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0,
            "2019": 0
        }
        for row in reader:
            try:
                year_count[row[5][-4:]] += 1
            except KeyError:
                print("Key error!")
                continue
            if "ao" in row[6]:
                found += 1


        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """main part of function to call all other functions"""
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
