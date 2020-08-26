"""
Improved performance
"""

import datetime
import csv

year_count = {
    "2013": 0,
    "2014": 0,
    "2015": 0,
    "2016": 0,
    "2017": 0,
    "2018": 0
}


def contains_ao(row):
    '''
    Method that gets passed to filter method.  Does two things.
    1) Updates year count appropriately
    2) Filters out rowns that don't contain "ao" value in the 7th poisiton

    :param row: Row to be evaluated
    '''
    if row[5][6:] in year_count:
        year_count[row[5][6:]] += 1
    return row[6] == "ao"

def analyze(filename):
    '''
    Loads data and counts number of entries between 2013-2018 and
    if the file contains ao in the 7th position

    :param filename: Fully qualified ame of file that contains data
    '''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        has_ao = list(filter(contains_ao, reader))
        found = len(has_ao)
        print(year_count)
        print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return (start, end, year_count, found)


def main():
    '''
    Executes program
    '''
    filename = "data/exercise_data.csv"
    result = analyze(filename)
    time = result[1] - result[0]
    print(time)


if __name__ == "__main__":
    main()
