"""
good-ly performing, good-ly written module
"""

import datetime
import csv
import logging
from timeit import timeit as timer
# pylint: disable=C0103, W0641, C0330
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze(filename):
    """Analyzes file for certain years and letters"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = {"2013": 0, "2014": 0, "2015": 0, "2016": 0, "2017": 0,
                      "2018": 0}
        found = [0]
        logger.info('Run time for counting years and filtering for "ao":'
                    ' %s sec', timer(
        '''for row in reader:
            if "ao" in row[6]:
                found[0] += 1

            try:
                year_count[row[5][6:]] += 1
            except KeyError:
                continue
        ''', globals=locals(), number=1))

        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """Calls and runs analye()"""
    logger.info('main() run time: %s sec', timer(
        'filename = "exercise.csv"\nanalyze(filename)', globals=globals(),
        number=1))

if __name__ == "__main__":
    logger.info('Program run time: %s sec', timer('main()', globals=globals(),
                                                  number=1))
