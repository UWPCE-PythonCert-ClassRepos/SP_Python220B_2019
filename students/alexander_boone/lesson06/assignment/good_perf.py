"""
poorly performing, poorly written module

"""

import datetime
import csv
from timeit import repeat
from statistics import mean

def analyze(filename):
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
                year_count[row[5][6:]] +=1
            if "ao" in row[6]:
                found += 1

    print(year_count)
    end = datetime.datetime.now()
    print(f"'ao' was found {found} times")
    return (start, end, year_count, found)

def main():
    testcode = '''
filename = "data/new_exercise_data.csv"
analyze(filename)
    '''
    n = 3
    time=repeat(
        stmt=testcode,
        globals=globals(),
        repeat=n,
        number=1
    )

    print('Avg. of ' + str(n) + ' poor_perf timeit runs (s):')
    print(mean(time))


if __name__ == "__main__":
    main()
