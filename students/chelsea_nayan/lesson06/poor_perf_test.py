"""
poorly performing, poorly written module

"""


import datetime
import csv

def analyze(filename):
    '''doc_string'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        year_count = { # Intitilizes the dict for year count
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        found = 0

        for row in reader:
            try:
                year_count[row[5][6:]] += 1
            except KeyError: # ignore the years that do not count
                pass
            if "ao" in row[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise_million.csv" # Changes this
    analyze(filename)


if __name__ == "__main__":
    main()
