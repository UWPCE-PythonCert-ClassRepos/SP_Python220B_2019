"""
better performing and better written module

"""

import datetime
import csv

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        found = 0

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        for row in reader:
            year = row[5][6:]
            # if year == '2013': year_count["2013"] += 1
            # elif year == '2014': year_count["2014"] += 1
            # elif year == '2015': year_count["2015"] += 1
            # elif year == '2016': year_count["2016"] += 1
            # elif year == '2017': year_count["2017"] += 1
            # elif year == '2018': year_count["2017"] += 1
            if year in year_count: year_count[year] += 1
            if row[6] == "ao": found += 1
        
        print(year_count)
        print("'ao' was found {} times".format(found))
        end = datetime.datetime.now()

        return (start, end, year_count, found)

def main():
    #filename = "data/exercise.csv"
    filename = "exercise.csv"
    analyze(filename)

if __name__ == "__main__":
    import timeit
    print(timeit.repeat("main()",
                        setup="from __main__ import main",
                        number=10))
    # main()
