"""
good performing, good written module

"""
# Advanced Programming in Python -- Lesson 6 Assignment 1
# Jason Virtue
# Start Date 2/21/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation,too-many-locals,no-else-return,unused-variable

import timeit
import datetime
import csv

def analyze(filename):
    '''poor performing function call'''
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
        for row in reader:
            if row[5] > '00/00/2012':
                if row[5][6:] == '2013':
                    year_count["2013"] += 1
                if row[5][6:] == '2014':
                    year_count["2014"] += 1
                if row[5][6:] == '2015':
                    year_count["2015"] += 1
                if row[5][6:] == '2016':
                    year_count["2016"] += 1
                if row[5][6:] == '2017':
                    year_count["2017"] += 1
                if row[5][6:] == '2018':
                    year_count["2018"] += 1
            if "ao" in row[6]:
                found += 1

        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    '''Call Analyze statement and passes in csv file'''
    filename = "data/exercise.csv"
    analyze(filename)

print(timeit.timeit(main, number=1))

if __name__ == "__main__":
    main()
