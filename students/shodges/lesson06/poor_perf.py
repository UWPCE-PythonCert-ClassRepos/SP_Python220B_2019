"""
poorly performing, poorly written module

"""

import datetime
import csv
import random
import time
import uuid

def analyze(filename):
    """
    Analyze filename for data trends.
    """
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

def random_date(start_date='01/01/2010', end_date='12/31/2019'):
    """
    Generate a random date between start_date and end_date, and return in the same format.
    """
    start_time = time.mktime(time.strptime(start_date, '%m/%d/%Y'))
    end_time = time.mktime(time.strptime(end_date, '%m/%d/%Y'))
    random_time = start_time + random.random() * (end_time - start_time)
    return time.strftime('%m/%d/%Y', time.localtime(random_time))

def main():
    """
    Defines behavior for main script operation.
    """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
