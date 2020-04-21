"""
Replaced ao_count if statement with a count function.
"""

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

    for date in data.Date:
        year_count[date[-4:]] += 1
    print(year_count)

    ao_count = 0
    ao_count = list(data.a_o).count('ao')
    print(f"'ao' was found {ao_count} times")

    print(f'{time.time() - start} seconds')

    return (year_count, ao_count)

def main():
    """Run the functions."""

    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
