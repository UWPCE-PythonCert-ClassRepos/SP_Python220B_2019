"""
good performing, awesomely written module
"""

import datetime
import logging
import csv
from timeit import timeit as timer

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'good_perf.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

def analyze():
    """This method analyzed the input .csv file"""
    filename = "data/exercise.csv"
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        found = 0
        for row in reader:
            if "ao" in row[6]:
                found += 1
            try:
                year_count[row[5][6:]] += 1
            except KeyError:
                continue

        print(year_count)
        print(f"'ao' was found {found} times")

        end = datetime.datetime.now()

    return (start, end, year_count, found)

if __name__ == "__main__":
    LOGGER.debug("Full program time: %s seconds", timer(
        'analyze()', globals=globals(), number=1))
