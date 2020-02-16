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
        new_ones = []
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for new in new_ones:
            if new[0][6:] == '2013':
                year_count["2013"] += 1
            if new[0][6:] == '2014':
                year_count["2014"] += 1
            if new[0][6:] == '2015':
                year_count["2015"] += 1
            if new[0][6:] == '2016':
                year_count["2016"] += 1
            if new[0][6:] == '2017':
                year_count["2017"] += 1
            if new[0][6:] == '2018':
                year_count["2017"] += 1

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

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
