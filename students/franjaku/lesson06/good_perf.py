"""
better performing module

"""

import datetime
import csv

def analyze(filename):
    start = datetime.datetime.now()
    with open(filename, encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')

        # # Step 1: Remove pointless new list
        # new_ones = []
        # for row in reader:
        #     lrow = list(row)
        #     if lrow[5] > '00/00/2012':
        #         new_ones.append((lrow[5], lrow[0]))

        year_count = {
            '2013': 0,
            '2014': 0,
            '2015': 0,
            '2016': 0,
            '2017': 0,
            '2018': 0
        }

        found = 0
        year_count_keys = year_count.keys()

        # for new in new_ones:
        for row in reader:
            key = row[5][6:]
            if key in year_count_keys:
                year_count[key] += 1

            if 'ao' in row[6]:
                found += 1
            # if row[5] > '00/00/2012':
            #     new = row[5]
            #     # Indented block below
            #     if new[0][6:] == '2013':
            #         year_count['2013'] += 1
            #     if new[0][6:] == '2014':
            #         year_count['2014'] += 1
            #     if new[0][6:] == '2015':
            #         year_count['2015'] += 1
            #     if new[0][6:] == '2016':
            #         year_count['2016'] += 1
            #     if new[0][6:] == '2017':
            #         year_count['2017'] += 1
            #     if new[0][6:] == '2018':
            #         year_count['2018'] += 1
            # pass

        # print(year_count)
        # print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    # # Step 2: Incorporate in with open() above
    # with open(filename) as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #
    #     found = 0
    #
    #     for line in reader:
    #         lrow = list(line)
    #         if "ao" in line[6]:
    #             found += 1
    #
    #     print(f"'ao' was found {found} times")
    #     end = datetime.datetime.now()
    #     print(end-start)
    return (start, end, year_count, found)

def main():
    filename = "data/exercise.csv"
    print(analyze(filename))


if __name__ == "__main__":
    main()
