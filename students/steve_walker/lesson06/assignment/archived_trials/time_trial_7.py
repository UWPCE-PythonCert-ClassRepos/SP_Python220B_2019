"""
Replaced year_count loop over every row with loop over each year,
coupled with a count function.
"""

import datetime
import csv
import time
import pandas


def analyze(filename):
    """Count instances of each year and 'ao' in a csv file."""

    start = time.time()

    data = pandas.read_csv(filename)

    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    dates = [date[-4:] for date in data.Date]

    for year in year_count:
        year_count[year] = dates.count(year)

    print(year_count)

    ao_count = list(data.a_o).count('ao')
    print(f"'ao' was found {ao_count} times")

    print(f'{time.time() - start} seconds')

    return (year_count, ao_count)

def main():
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
