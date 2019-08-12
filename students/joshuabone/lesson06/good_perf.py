# pylint: disable=duplicate-code
"""
Better performing, better written module.
"""

import csv
import logging
from collections import defaultdict
import poor_perf

logging.basicConfig(level=logging.INFO)


def analyze(filename):
    """Analyze a CSV file line by line."""
    stopwatch = poor_perf.Stopwatch()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = defaultdict(int)
        ao_count = 0
        for line in reader:
            # Faster to increment for all years here and filter later.
            # Reading a string slice is faster than reading a datetime object.
            year_count[line[5][6:10]] += 1
            if line[6] == 'ao':
                ao_count += 1

        # Purge keys that are outside the date range of 2013-2018
        for key in set(year_count.keys()):
            if not '2012' < key < '2019':
                del year_count[key]

        time_diff = stopwatch.mark()
        logging.info("Time elapsed: %f secs.", time_diff)
        logging.info(year_count)
        logging.info("'ao' was found %d times", ao_count)

    return year_count, ao_count


if __name__ == "__main__":
    analyze("data/lesson06.csv")
