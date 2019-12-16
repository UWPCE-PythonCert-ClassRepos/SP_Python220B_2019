""" Better written module to analyze CSV file """

import datetime
import csv

def analyze(filename):
    """ Analyze the data in the CSV file """

    # Note the current date/time stamp
    start = datetime.datetime.now()

    # Initialize a dictionary to count specific years
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }

    # Initialize a counter for the 'ao' field
    found = 0

    # Open the CSV file and count instances
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            lrow = list(row)
            if int(lrow[5][6:]) > 2012 and int(lrow[5][6:]) < 2019:
                year_count[lrow[5][6:]] += 1
            if "ao" in lrow[6]:
                found += 1

        print(year_count)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """ Main function to start analysis """

    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
