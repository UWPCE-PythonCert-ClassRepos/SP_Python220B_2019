"""
poorly performing, poorly written module

"""

import datetime
import csv

#def year_2012(row):
#    if row[5] > '00/00/2012':
#        return (row[5], row[0])


def analyze(filename):
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
#        new_ones = []
#        new_ones = {}
#        new_ones = [(row[5], row[0]) for row in reader if row[5] > '00/00/2012']
        new_ones = {row[0]:row[5][6:] for row in reader if row[5] > '00/00/2012'}
#        for row in reader:
#            lrow = list(row)
#            if lrow[5] > '00/00/2012':
#                new_ones[lrow[0]] = lrow[5][6:]
#                new_ones.append((lrow[5], lrow[0]))

        year_2013 = list(new_ones.values()).count('2013')
        year_2014 = list(new_ones.values()).count('2014')
        year_2015 = list(new_ones.values()).count('2015')
        year_2016 = list(new_ones.values()).count('2016')
        year_2017 = list(new_ones.values()).count('2017')
        year_2018 = list(new_ones.values()).count('2018')

        year_count = {
            "2013": year_2013,
            "2014": year_2014,
            "2015": year_2015,
            "2016": year_2016,
            "2017": year_2017,
            "2018": year_2018
        }

#        for new in new_ones:
#            if new[0][6:] == '2013':
#                year_count["2013"] += 1
#            if new[0][6:] == '2014':
#                year_count["2014"] += 1
#                year_count["2015"] += 1
#            if new[0][6:] == '2016':
#                year_count["2016"] += 1
#            if new[0][6:] == '2017':
#                year_count["2017"] += 1
#            if new[0][6:] == '2018':
#                year_count["2018"] += 1

        print(year_count)

    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

#        found = 0

#        for line in reader:
#            lrow = list(line)
#            if "ao" in line[6]:
#                found += 1

        found = [line[6] for line in reader if line[6] == 'ao'].count('ao')


        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    analyze(filename)


if __name__ == "__main__":
    main()
