"""
good performing, good written module
"""

import datetime
import csv

def analyze(filename):
    """Analysis on given csv file"""
    # Get starting time
    start = datetime.datetime.now()
    # Initialize each year count
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    # Initialize the occurences of 'ao'
    found = 0
    # Open csv file for reading
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Loop thru each row
        for row in reader:
            try:
                # Count all records with 2012 < year < 2019
                if (int(row[5][6:]) > 2012 and int(row[5][6:]) < 2019):
                    year_count[row[5][6:]] += 1
                # Count all records with 'ao' in it
                if "ao" in row[6]:
                    found += 1
            except IndexError:
                pass

    # Display result
    print(year_count)
    print("'ao' was found {} times".format(found))

    # Get starting time
    end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """Main function"""
    filename = "data/exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    # Call main function
    main()
