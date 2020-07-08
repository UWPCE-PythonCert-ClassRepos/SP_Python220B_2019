"""
    Process data file.
"""


import datetime
import csv
from timeit import timeit as timer

def analyze(filename):
    """
        Des: analyze data file
        In:  target fileaname to analyze
        Out: tuple of analyzed data stats (start,end,year,found)
    """

    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
    
        year_count = {
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
            if "ao" in row[6]:
                found += 1
            try:
                year_count[row[5][6:]] += 1
            except KeyError:
                continue
        
        print(year_count)
        print(f"'ao' was found {found} times")

    end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    #filename = "data/exercise.csv"
    #analyze(filename)
    print(timer(
    'perfomance = analyze(FILENAME)',
    globals=globals(),
    number=1))



if __name__ == "__main__":
    FILENAME = "data/exercise.csv"
    main()
