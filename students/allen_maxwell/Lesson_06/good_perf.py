'''Better performing, better written module'''

import datetime
import csv

def analyze(filename):
    '''Analyzes a datatbase file'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = {'2013': 0, '2014': 0, '2015': 0, '2016': 0, '2017': 0, '2018': 0}
        found = 0

        for new in reader:
            if new[6] == 'ao':
                found += 1
            try:
                year_count[new[5][6:]] += 1
            except KeyError:
                continue

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

if __name__ == "__main__":
    FILENAME = "data/exercise.csv"
    analyze(FILENAME)
