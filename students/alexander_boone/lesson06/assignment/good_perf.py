"""
poorly performing, poorly written module

"""

import datetime
import csv
from timeit import repeat
from statistics import mean


def analyze(filename):
    '''
    Analyze csv file to sum counts of lines with each year
    and count the amount of 'ao' strings at the row's end.
    '''
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        for row in reader:
            if row[5] in year_count.keys():
                year_count[row[5][6:]] += 1
            if "ao" in row[6]:
                found += 1

    print(year_count)
    end = datetime.datetime.now()
    print(f"'ao' was found {found} times")
    return (start, end, year_count, found)


def main():
    '''Run main function code.'''
    testcode = '''
filename = "data/new_exercise_data.csv"
analyze(filename)
    '''
    n_repeats = 3
    time = repeat(
        stmt=testcode,
        globals=globals(),
        repeat=n_repeats,
        number=1
    )

    print('Avg. of ' + str(n_repeats) + ' poor_perf timeit runs (s):')
    print(mean(time))


if __name__ == "__main__":
    main()
