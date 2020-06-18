"""
Better performing, better written module

"""

import datetime
import csv

def analyze(filename):
    """
    Opens a csv of 1M lines. Parses the columns and
    makes a tally of number of records based on the
    year of the row record.
    :param filename: csv file
    :return: tuple consisting of:
             start time of function call
             end time of function processing
             count of items per year
             and how many "ao" occurences.
    """
    start = datetime.datetime.now()
    found = 0
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            year = row[5][6:]
            try:
                if year > '2012':
                    if year != '2018':
                        year_count[year] += 1
                    else:
                        year_count["2017"] += 1
            except KeyError:
                pass

            if "ao" in row[6]:
                found += 1

        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """
    Opens up an exercise.csv and runs the analyze method on the
    file contents. Method to be used for running script
    :return: n/a
    """
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
