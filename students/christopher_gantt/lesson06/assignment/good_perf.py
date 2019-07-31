"""better performing, better written module"""

import datetime
import csv
# import time

# init = time.perf_counter()

def main():
    '''
        Analyzes data from a csv file.
        Returns a tuple with (the datetime when the script starts,
                              the datetime when the script ends,
                              a dict with year counts,
                              'ao' found number)
    '''
    start = datetime.datetime.now()
    with open("data/exercise.csv") as csvfile:
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
            if "ao" in row[6]:
                found += 1
            try:
                year_count[row[5][6:]] += 1
            except KeyError:
                continue

        print(year_count)
        print(f"'ao' was found {found} times")

    end = datetime.datetime.now()

    return (start, end, year_count, found)

if __name__ == "__main__":
    main()

# print(time.perf_counter()-init)
