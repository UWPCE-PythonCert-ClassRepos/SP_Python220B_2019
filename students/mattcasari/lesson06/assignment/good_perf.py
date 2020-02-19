"""
better performing, better written module

"""

import datetime
import csv

def _counter():
    idx = 0
    while True:
        yield idx
        idx += 1

def analyze(filename):
    start = datetime.datetime.now()
    found = _counter()
    year_count = dict.fromkeys([str(x) for x in range(2010,2021)],0)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')        
        for row in reader:
            year_count[row[5][6:]] += 1
            if "ao" in row[6]:
                next(found)
                         
        found = next(found)

        end = datetime.datetime.now()
        
    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
