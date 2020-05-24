
""" Good performance script for lesson06's assignment"""

import datetime
import csv

def analyze(filename):
    """ opens csv file and counts the years and 'ao' in the same loop """
    start = datetime.datetime.now()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0}
    aofound = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            year = row[5][:4]
            if year == '2013':
                year_count["2013"] += 1
            elif year == '2014':
                year_count["2014"] += 1
            elif year == '2015':
                year_count["2015"] += 1
            elif year == '2016':
                year_count["2016"] += 1
            elif year == '2017':
                year_count["2017"] += 1
            elif year == '2018':
                year_count["2018"] += 1
            if row[6]:
                aofound += 1
    print(year_count)
    print(f"'ao' was found {aofound} times")
    end = datetime.datetime.now()
    print(end - start)

if __name__ == "__main__":
    analyze('exercise.csv')
