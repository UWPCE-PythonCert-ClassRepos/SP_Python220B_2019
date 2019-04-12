"""
poorly performing, poorly written module
"""

import datetime
import csv
import logging
from timeit import timeit as timer
# pylint: disable=C0330, W0641, C0111, C0103
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        logger.info('run time for row reader and filter for > 00/00/2012:'
                    ' %s sec', timer(
        '''for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))''', globals=locals(),
                number=1))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        logger.info('Sorting and counting matching years run time: %s sec',
                    timer(
        '''for new in new_ones:
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
            if new[0][6:] == '2018': #new[0][6:] == 00/00/2012.....2012
                year_count["2017"] += 1''', globals=locals(), number=1))

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = [0]
        logger.info('run time for reading and filtering for "ao": %s sec',
                    timer(
        '''for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found[0] += 1''', globals=locals(), number=1))
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    logger.info('main() run time: %s sec', timer(
        'filename = "exercise.csv"\nanalyze(filename)', globals=globals(),
        number=1))


if __name__ == "__main__":
    logger.info('Program run time: %s sec', timer('main()', globals=globals(),
    number=1))
