"""
Introduced panda reader to limit the data we read in the csv to two columns.
"""

import datetime
import csv
import time
import pandas

def analyze(filename):
    """Count instances of each year and 'ao' in a csv file."""

    start = time.time()

    data = pandas.read_csv(filename)
#    with open(filename) as csvfile:
#        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    ao_count = 0
    print(data.Date[0])
  
    for date in data.Date:
        year_count[date[-4:]] += 1

    for cell in data.a_o:
        if 'ao' in str(cell):
            ao_count += 1

    print(year_count)
    print(f"'ao' was found {ao_count} times")

    print(f'{time.time() - start} seconds')

    return (year_count, ao_count)

def main():
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
