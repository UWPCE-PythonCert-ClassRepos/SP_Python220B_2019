"""
poorly performing, poorly written module

"""

import datetime
import csv
import time
import logging
import datetime
import timeit


"""logging setup"""
LOG_FORMAT = '%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s'
FORMATTER = logging.Formatter(LOG_FORMAT)

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '-good_perf.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)


LOGS = logging.getLogger()
LOGS.setLevel(logging.INFO)
if not LOGS.hasHandlers():
    LOGS.addHandler(FILE_HANDLER)


def year_filter_function(input):
    return "2019" > input[5][-4:] > "2012"


def ao_filter_function(input):
    return input == "ao"


def year_count_function(input):
    dict, row = input
    dict[row[5][-4:]] += 1


def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        init1 = time.process_time()
        new_ones = list(filter(year_filter_function, reader))
        LOGS.info(f"\n time for the for filtering block: {time.process_time() - init1} and found {len(new_ones)} items")
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        init2 = time.process_time()
        list(map(year_count_function, [(year_count, x) for x in new_ones]))
        print(year_count)
        LOGS.info(f"\n time for the for block counting years: {time.process_time() - init2}")

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0
        init3 = time.process_time()
        ao_list = list(filter(ao_filter_function, [x[6] for x in reader]))
        print(f"'ao' was found {len(ao_list)} times")
        LOGS.info(f"\n time for the for block counting ao: {time.process_time() - init3}")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    LOGS.info("NEW RUN")
    init = time.process_time()
    main()
    LOGS.info(f'\ntime to run 1 full loop:{time.process_time() - init}')


