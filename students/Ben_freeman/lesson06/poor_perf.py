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

LOG_FILE = datetime.datetime.now().strftime("%Y-%m-%d") + '-poor_perf.log'

FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.INFO)


LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
if not LOG.hasHandlers():
    LOG.addHandler(FILE_HANDLER)


def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        init1 = time.process_time()
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))
        LOG.info(f"\n time for the for filtering block: {time.process_time() - init1} and found {len(new_ones)} items")
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        init2 = time.process_time()
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

        print(year_count)
        LOG.info(f"\n time for the for block counting years: {time.process_time() - init2}")

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0
        init3 = time.process_time()
        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        print(f"'ao' was found {found} times")
        LOG.info(f"\n time for the for block counting ao: {time.process_time() - init3}")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    LOG.info("NEW RUN")
    init = time.process_time()
    main()
    LOG.info(f'\ntime to run 1 full loop:{time.process_time() - init}')
