
"""
Victor Medina
Enhanced python file
"""

import datetime
import csv
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def analyze(filename):
    """

    :param filename:
    :return:
    """
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
            if row[5][6:] == '2013':
                year_count["2013"] += 1
            elif row[5][6:] == '2014':
                year_count["2014"] += 1
            elif row[5][6:] == '2015':
                year_count["2015"] += 1
            elif row[5][6:] == '2016':
                year_count["2016"] += 1
            elif row[5][6:] == '2017':
                year_count["2017"] += 1
            elif row[5][6:] == '2018':
                year_count["2018"] += 1

        LOGGER.info(year_count)
        LOGGER.info('ao was found {} times'.format(found))
        end = datetime.datetime.now()
    LOGGER.info(end - start)
    return start, end, year_count, found


def main():
    """

    :return:
    """

    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
