'''
Advanced Programming in Python Lesson 6
Finding Bottlenecks

good_perf module: increase performance of poor_perf.py with same results
'''

import csv

def main(filename):
    '''
    open csv, count quantity of years stated below and if ao exist in row
    '''


    year_results = {
                    '2013': 0,
                    '2014': 0,
                    '2015': 0,
                    '2016': 0,
                    '2017': 0,
                    '2018': 0
                    }

    ao_result = 0


    with open(filename) as csvfile:
        data = csv.reader(csvfile)

        for row in data:
            if (row[5][6:]) in year_results.keys():
                year_results[(row[5][6:])] += 1
            if (row[6]):
                ao_result += 1

        print(year_results)
        print(f"'ao' was found {ao_result} times")


if __name__ == "__main__":
    filename = "data/exercise.csv"
    main(filename)