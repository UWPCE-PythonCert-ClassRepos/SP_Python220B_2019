# pylint: disable=duplicate-code
"""
poorly performing, poorly written module

"""

import csv
import logging
import time


logging.basicConfig(level=logging.INFO)


class Stopwatch:  # pylint: disable=too-few-public-methods
    """Simple stopwatch for timing events."""
    def __init__(self):
        self.last = time.time_ns()

    def mark(self):
        """Reset the clock time and return time elapsed."""
        now = time.time_ns()
        diff = (now - self.last) / 1_000_000_000
        self.last = now
        return diff


def analyze(filename):
    """Analyze a CSV file line by line."""
    stopwatch = Stopwatch()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        new_ones = []
        for row in reader:
            lrow = list(row)
            if lrow[5] > '00/00/2012':
                new_ones.append((lrow[5], lrow[0]))

        time_diff = stopwatch.mark()
        logging.info("Filter years > 2012: %f secs.", time_diff)

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

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

        time_diff = stopwatch.mark()
        logging.info("Year counts: %f secs.", time_diff)
        logging.info(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        found = 0

        for line in reader:
            lrow = list(line)
            if "ao" in line[6]:
                found += 1

        logging.info("'ao' was found %d times", found)

    time_diff = stopwatch.mark()
    logging.info("Count 'ao' occurrences: %f secs.", time_diff)

    return year_count, found


def main():
    """Main method for poor_perf.py"""
    filename = "data/lesson06.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
