"""
greatly performing, greatly written module

"""
#pylint: disable=duplicate-code
import datetime
import csv

def analyze(filename):
    '''
    This module analyzes the csv file and returns the
    number of times each year shows and and number of
    times ao shows up
    '''
    start = datetime.datetime.now()

    with open(filename) as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        #not needed
        #new_ones = []
        found = 0

        #moved up before row loop
        year_count = {"2013": 0,
                      "2014": 0,
                      "2015": 0,
                      "2016": 0,
                      "2017": 0,
                      "2018": 0}
        year_keys = year_count.keys()
        for row in reader:
            #list assignment below no longer needed
            #lrow = list(row)

            if "ao" in row[6]:
                found += 1
            year = row[5][6:]
            if year in year_keys:
                year_count[year] += 1
            #if statement no longer needed
            #if lrow[5] > '00/00/2012':
            #   new_ones.append((lrow[5], lrow[0]))

        #takes more time to individually loop through each row
        #and conditionally check each year
        #commenting out loop below
        #for new in new_ones:
        #    if new[0][6:] == '2013':
        #        year_count["2013"] += 1
        #    if new[0][6:] == '2014':
        #        year_count["2014"] += 1
        #    if new[0][6:] == '2015':
        #        year_count["2015"] += 1
        #    if new[0][6:] == '2016':
        #        year_count["2016"] += 1
        #    if new[0][6:] == '2017':
        #        year_count["2017"] += 1
        #    if new[0][6:] == '2018':
        #        year_count["2018"] += 1

        print(year_count)

    #combine ao count with year count above
    #without re-opening file

    #with open(filename) as csvfile:
    #    reader = csv.reader(csvfile, delimiter=',', quotechar='"')

    #    found = 0

    #    for line in reader:
    #        lrow = list(line)
    #        if "ao" in line[6]:
    #           found += 1

        print(f"'ao' was found {found} times")

    end = datetime.datetime.now()
    return (start, end, year_count, found)

def main():
    '''
    Main module
    '''
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
