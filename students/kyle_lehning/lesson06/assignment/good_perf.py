"""
good performing, well written module
"""

import datetime
import csv
import logging
import time
from timeit import timeit as timer


def __setup_logger(name, log_file, level=logging.WARNING, stream=True):
    """
    This function sets up loggers.
    """
    log_format = logging.Formatter("%(asctime)s%(filename)s:%(lineno)-3d %(levelname)s %(message)s")
    handler = logging.FileHandler(log_file)
    handler.setFormatter(log_format)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    if stream is True:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        logger.addHandler(stream_handler)
    return logger


LOG_FILE = 'good_perf' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('database_logger', LOG_FILE, logging.INFO)


def analyze(filename):
    """
    Analyse the dates and the count of ao in passed file. Return the start time, end time, a
    dictionary with the year count, and an integer of the number of times ao was found
    """
    start = datetime.datetime.now()
    first_open_start = time.time()
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
        for_start = time.time()
        for row in reader:
            lrow = list(row)
            if int(lrow[5][6:]) > 2012:
                year_count[lrow[5][6:]] += 1
            if "ao" in row[6]:
                found += 1
        print(f"'ao' was found {found} times")
        for_end = time.time()
        end = datetime.datetime.now()
        print(year_count)
    first_open_end = time.time()
    LOGGER.info('First open time: %s', first_open_end - first_open_start)
    LOGGER.info('For Loop with elifs: %s', for_end - for_start)
    return start, end, year_count, found


def main():
    """Run analyse on data/exercise.csv"""
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    LOGGER.info('timeit run: %s', timer('main()', globals=globals(), number=10))
