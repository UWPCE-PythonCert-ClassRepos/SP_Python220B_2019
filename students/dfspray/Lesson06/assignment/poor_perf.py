"""
poorly performing, poorly written module
I modified this to include timers in certain areas to analyze the program
"""

import datetime
import logging
import csv
from timeit import timeit as timer

# pylint: disable=W0621, W0641, W0612

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'poor_perf.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

def analyze(filename):
    """This method analyzed the input .csv file"""
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        LOGGER.debug("Appending to new_ones for loop: %s seconds", timer(
            """for row in reader:
                lrow = list(row)
                if lrow[5] > '00/00/2012':
                    new_ones.append((lrow[5], lrow[0]))""",
            globals=locals(), number=1))

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        LOGGER.debug("Counting year frequency with if filter: %s seconds", timer(
            """for new in new_ones:
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
                    year_count["2018"] += 1""",
            globals=locals(), number=1))

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
    """This is the main method that calls 'analyze'"""
    LOGGER.debug("main() method time: %s seconds", timer(
        'filename = "data/exercise.csv"\nanalyze(filename)', globals=globals(), number=1))

if __name__ == "__main__":
    LOGGER.debug("Full program time: %s seconds", timer(
        'main()', globals=globals(), number=1))
