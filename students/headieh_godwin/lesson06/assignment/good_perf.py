"""
better performing, better written module
"""
import datetime
import csv

def analyze(filename):
    """
    returns counts of years 2013-2018, and counts of ao
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }
        found = 0
        for row in reader:
            if row[5][6:] in year_count.keys():
                year_count[row[5][6:]] += 1
            if row[6] == 'ao':
                found += 1
        print(year_count)
        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()
    return (start, end, year_count, found)

def main():
    """
    reads file and runs analyze
    """
    filename = "data/exercise_million.csv"
    analyze(filename)

if __name__ == "__main__":
    main()
