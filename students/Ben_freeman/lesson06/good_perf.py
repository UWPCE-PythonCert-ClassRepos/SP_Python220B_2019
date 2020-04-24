"""
goodlyer performing, still poorly written module

"""

import csv
import time
import logging
import datetime


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


def filter_function(input1):
    """filters"""
    input2, list_ao, list_year = input1
    if "2019" > input2[5][-4:] > "2012" and input2[6] == "ao":
        list_ao.append(input2)
        list_year.append(input2)
    elif "2019" > input2[5][-4:] > "2012":
        list_year.append(input2)
    elif input2[6] == "ao":
        list_ao.append(input2)


def year_count_function(input1):
    """counts"""
    dict1, row = input1
    dict1[row[5][-4:]] += 1


def analyze(filename):
    """does all of the work"""
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        init1 = time.process_time()
        ao_list = []
        new_ones = []
        list(map(filter_function, [(x, ao_list, new_ones) for x in reader]))
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

        print(f"'ao' was found {len(ao_list)} times")




def main():
    """feels redundant"""
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    LOGS.info("NEW RUN")
    init = time.process_time()
    main()
    LOGS.info(f'\ntime to run 1 full loop:{time.process_time() - init}')
    FILE_HANDLER.close()
