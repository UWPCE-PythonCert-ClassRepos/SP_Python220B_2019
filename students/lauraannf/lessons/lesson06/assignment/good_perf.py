"""
poorly performing, poorly written module

"""

import datetime
import csv
import time


def analyze(filename):
    """open and analyze csv file"""
    start = datetime.datetime.now()
    start_open1 = time.clock()
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

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
    print(f"first open csv time : {time.clock() - start_open1}")
    return (start, end, year_count, found)


def main():
    """main function"""
    filename = "data/exercise2.csv"
    start_analyze = time.clock()
    analyze(filename)
    print('time of analyze function: {}'.format(time.clock() - start_analyze))


if __name__ == "__main__":
    main()
