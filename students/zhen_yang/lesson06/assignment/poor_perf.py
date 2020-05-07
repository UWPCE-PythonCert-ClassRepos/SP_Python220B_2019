"""
poorly performing, poorly written module

"""

import datetime
import csv
import logging
import time
import cProfile
import pstats

# set logging configuration
LOG_FORMAT = "%(levelname)s %(filename)s %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def analyze(filename):
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
                year_count["2018"] += 1

        #print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        #print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    # print(f'start time:{start}')
    # print(f'end time:{end}')
    # print(f'year_count:{year_count}')
    # print(f'found "ao":{found}')
    return (start, end, year_count, found)

def main():
    #filename = "data/exercise.csv"
    #analyze(filename)

    cProfile.run('analyze("data/exercise_new.csv")', 'analyze_poor.res')
    with open('time_poor.res', 'w') as file:
        q = pstats.Stats('analyze_poor.res', stream=file)
        q.strip_dirs().sort_stats('time').print_stats(10)

if __name__ == "__main__":
    main()
