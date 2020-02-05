"""
poorly performing, poorly written module

"""

import datetime
import csv



def analyze(filename):
    """Iterate over .csv file to get the count of entries with in the year range
       below and count ao entries"""

    start = datetime.datetime.now()
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        found = 0
        year_count = dict.fromkeys(range(2010, 2020), 0)
        for row in reader:
            if 'ao' in row[6]:
                found += 1
            year_count[int(row[5][6:])] += 1
    year_count = {k: year_count.get(k, None) for k in range(2012, 2019)}
    end = datetime.datetime.now()
    return (start, end, year_count, found)


def main():
    """Assign filename and print info"""
    filename = "records.csv"
    (start, end, year_count, found) = analyze(filename)
    print(f"started at:{start}")
    print(f"ended at:  {end}")
    print(f"Total elapsed: {end-start}")
    print(year_count)
    print(f"'ao' was found {found} times")


if __name__ == "__main__":
    main()
