"""
poorly performing, poorly written module

"""

import datetime
import csv
# import time


def analyze(filename):
    """
    Glean metrics on count of years occuring, and count of ao.
    """
    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        #VV ORIGINAL LOOP VV
        # init = time.process_time()
        # new_ones = []
        # for row in reader:
        #     lrow = list(row)
        #     if lrow[5] > '00/00/2012':
        #         new_ones.append((lrow[5], lrow[0]))
        # print('append loop = ', time.process_time() - init)

        #VV COMPREHENSION ATTEMPTED, NO TIME IMPROVEMENT VV
        # init = time.process_time()
        # new_ones = [(row[5], row[0]) for row in reader if row[5] > '00/00/2012']
        # print('append comprehension = ', time.process_time() - init)

        #VV MAP-FILTER WITH FUNCTIONS ATTEMPTED, NO TIME IMPROVEMENT VV
        # init = time.process_time()

        # def date_and_guid(row):
        #     return (row[5], row[0])

        # def new_date(row):
        #     return row[5] > '00/00/2012'

        # new_ones = list(map(date_and_guid, filter(new_date, reader)))
        # print('map filter with functions = ', time.process_time() - init)

        #VV MAP-FILTER WITH LAMBDAS ATTEMPTED, NO TIME IMPROVEMENT VV
        # init = time.process_time()
        # new_ones = list(map(lambda row: (row[5], row[0]),
        #                     filter(lambda row: row[5] > '00/00/2012', reader)))
        # print('map filter with lambda = ', time.process_time() - init)

        year_count = {
            "2013": 0,
            "2014": 0,
            "2015": 0,
            "2016": 0,
            "2017": 0,
            "2018": 0
        }

        #VV COMBINED ALL LOOPS, NOTABLE TIME IMPROVEMENT VV
        # init = time.process_time()
        # new_ones = []
        # found = 0
        # for row in reader:
            # if row[5] > '00/00/2012':
            #     new_ones.append((row[5], row[0]))
        #     if "ao" in row[6]:
        #         found += 1
        #     if '2012' < row[5][6:]:
        #         year_count[row[5][6:]] += 1
        # print('combined new_ones, year_count, and ao loop = ', time.process_time() - init)

        #VV COMBINED NECESSARY LOOPS, REMOVED EXTRANEOUS LOOP, REMOVED EXTRANEOUS LIST. VV
        found = 0
        for row in reader:
            if "ao" in row[6]:
                found += 1
            if row[5][6:] > '2012':
                year_count[row[5][6:]] += 1

        #VV ORIGINAL LOCATION OF DICT VV
        # year_count = {
        #     "2013": 0,
        #     "2014": 0,
        #     "2015": 0,
        #     "2016": 0,
        #     "2017": 0,
        #     "2018": 0
        # }

        #VV ORIGINAL LOGIC FOR YEAR COUNT VV
        # init = time.process_time()
        # for new in new_ones:
        #     if new[0][6:] == '2013':
        #         year_count["2013"] += 1
        #     if new[0][6:] == '2014':
        #         year_count["2014"] += 1
        #     if new[0][6:] == '2015':
        #         year_count["2015"] += 1
        #     if new[0][6:] == '2016':
        #         year_count["2016"] += 1
        #     if new[0][6:] == '2017':
        #         year_count["2017"] += 1
        #     if new[0][6:] == '2018':
        #         year_count["2018"] += 1
        # print('year loop = ', time.process_time() - init)

        print(year_count)

    #VV AO LOOP WITH EXTRANEOUS LIST REMOVED, SMALL TIME IMPROVEMENT VV
    # with open(filename) as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        # init = time.process_time()
        # found = 0
        # for line in reader:
        #     if "ao" in line[6]:
        #         found += 1
        # print('ao loop = ', time.process_time() - init)

        print(f"'ao' was found {found} times")
        end = datetime.datetime.now()

    return (start, end, year_count, found)


if __name__ == "__main__":
    FILENAME = "data/exercise.csv"
    analyze(FILENAME)
