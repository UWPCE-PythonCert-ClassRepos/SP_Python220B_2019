"""
better performing, well written module

"""

import datetime
import csv
import sys

def analyze(filename):
    '''
    Method to read csv file and count the number of records that reference
    a particular year, and the occurences of 'ao' in the last field

    Args:
        filename (str):
            CSV file to process

    Returns:
        start (datetime object):
            Start time when program was run
        end (datetime object):
            End time when program was run
        year_count (dict):
            Dictionary containing year counts (key = string representation of
            year, value = count of year)
        found (int):
            Count of the number of records that contained 'ao' in the last field
    '''
    start = datetime.datetime.now()
    try:
        with open(filename) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            found = 0
            year_count = {key:0 for key in map(str, range(2013, 2019))}

            for row in reader:
                year = row[5][-4:]
                if year > '2012':
                    year_count[year] += 1
                if 'ao' in row[-1]:
                    found += 1

    except FileNotFoundError:
        print('Error, {} not found. Check file location.'.format(filename))
        sys.exit()
    except IOError:
        print('Error reading {}. Check file contents and permissions.'.format(filename))
        sys.exit()

    print(year_count)
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    '''
    Main function, will run analyze function with a default csv file.
    '''
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
