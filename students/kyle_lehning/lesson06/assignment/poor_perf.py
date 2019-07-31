"""
poorly performing, poorly written module

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


LOG_FILE = 'poor_perf' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log'
LOGGER = __setup_logger('database_logger', LOG_FILE, logging.INFO)


def analyze(filename):
    start = datetime.datetime.now()
    first_open_start = time.time()
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
        for_start = time.time()
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
        for_end = time.time()
        print(year_count)
    first_open_end = time.time()
    LOGGER.info('First open time: %s', first_open_end - first_open_start)
    LOGGER.info('For loop with ifs: %s', for_end - for_start)
    second_open_start = time.time()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
    second_open_end = time.time()
    LOGGER.info("Second open time: %s", second_open_end - second_open_start)
    LOGGER.info("Total time: %s", second_open_end - first_open_start)
    return (start, end, year_count, found)


def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    LOGGER.info('timeit run: %s', timer('main()', globals=globals(), number=10))
