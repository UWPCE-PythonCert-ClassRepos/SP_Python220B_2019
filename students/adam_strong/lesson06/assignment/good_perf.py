"""
Better performing module, original file clocked in at:

    Starting File: ~2.666 seconds (Python3)
    Ending File: ~1.360 seconds (Python3) and 0.619 seconds (PyPy)
    Commented out the print statements for Python2/PyPy

Added a print statement for total time in the function.

"""

import datetime
import csv


def analyze(filename):
    '''Run through a csv and create a dict for years and
    a string for found 'ao' instances'''
    start = datetime.datetime.now()
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0
    }
    found = 0

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
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


            if 'ao' in row[6]:
                found += 1
        #print year_count # For Python2
        #print "'ao' was found " + str(found) + " times" # For Python2
        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    #print 'Total time: ' + str(end-start) # For Python2
    print('Total time: ', end-start)
    return (start, end, year_count, found)

def main():
    '''Run the analysis script with chosen csv'''
    filename = "data/random_million_rows.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
