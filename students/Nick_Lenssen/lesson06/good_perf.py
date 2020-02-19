"""Read in data from .csv file to count year number and count
the amount of times ao happens"""

import datetime
import csv
from timeit import timeit as timer

def analyze(filename):
    """function to open the csv and count the data"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        count = 0

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
            if row[6] == 'ao':
                count += 1 #counts the amount of ao's occur
            try:
                year_count[row[5][6:]] += 1 #adds one to the year
            except KeyError:
                pass

        print(year_count)

        print('"ao" found {} times'.format(count))

        end = datetime.datetime.now()

        return (start, end, year_count, count)

def main():
    """print out the performance"""
    print(timer(
        'good_perfomance = analyze(FILENAME)',
        globals=globals(),
        number=1))

if __name__ == "__main__":
    FILENAME = "data/exercise.csv"
    main()
    