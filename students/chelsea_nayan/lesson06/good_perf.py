'''Better performing, better written module'''

#lesson06

# Checklist:
# (1) Rewrite the module to improve performanc
# (2) Provide evidence to demonstrate improvement - .txt file?
# (3) Use identical input and output to poor_perf.py

import datetime
import csv

def analyze(filename):
    '''Returns year and ao count from a csv file'''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        year_count = {"2013": 0,
                      "2014": 0,
                      "2015": 0,
                      "2016": 0,
                      "2017": 0,
                      "2018": 0}

        ao_count = 0

        for row in reader:
            try:
                year_count[row[5][6:]] += 1
            except KeyError: # ignore the years that do not count
                pass
            if row[6] == 'ao':
                ao_count += 1

        print(year_count)
        print(f'"ao" was found {ao_count} times')

        end = datetime.datetime.now()

    return (start, end, year_count, ao_count)

def main():
    '''Run analyze function'''
    filename = 'data/exercise_million.csv'
    analyze(filename)

if __name__ == '__main__':
    main()
