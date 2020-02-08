""" lesson06 code rewrite
"""

import csv
import timeit


def analyze(filename):
    """ Call process_file and count_years. Return the year count dict from count_years and the 'ao'
    count from process_file.

    Arguments:
    filename - csv file name with data
    """
    dates, found_ao = process_file(filename)
    year_count = count_years(dates)
    return (year_count, found_ao)

def process_file(filename):
    """ Read a csv file that has a date in the 6th column and an optional 'ao' string in the 7th
    column. Append the dates to a list and count the number of records with the 'ao' string in the
    7th column. Print the 'ao' count. Return the list with dates and the 'ao' count.

    Arguments:
    filename - csv file name with data
    """

    dates = []
    found = 0
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            lrow = list(row)
            dates.append(lrow[5])

            if "ao" in row[6]:
                found += 1

    print(f"'ao' was found {found} times")
    return dates, found


def count_years(dates):
    """ Count each year in a list of formatted dates, print a dict with members of the form
    year: count for the years greater than 2013, and return it.

    Arguments:
    dates - a list of dates of the form MM-DD-YYYY
    """
    year_count = {"2010": 0,
                  "2011": 0,
                  "2012": 0,
                  "2013": 0,
                  "2014": 0,
                  "2015": 0,
                  "2016": 0,
                  "2017": 0,
                  "2018": 0,
                  "2019": 0}

    for date in dates:
        year_count[date[6:]] += 1

    # To keep this strictly the same as the original, which only counted for years starting with
    # 2013, delete 2010, 2011, & 2012 from the dictionary.
    year_count.pop("2010")
    year_count.pop("2011")
    year_count.pop("2012")

    print(year_count)
    return year_count


def main():
    """ Time the program and save the results to a file.
    """

    with open("good_performance.txt", 'w', newline='') as file:
        times = []
        for i in range(10):
            time = timeit.timeit('analyze("lesson06_data.csv")',
                                 setup="from __main__ import analyze",
                                 number=1,
                                 globals=globals())
            print(time)
            times.append("{}.,{}\n".format(i + 1, time))

        file.writelines(times)


if __name__ == "__main__":
    main()
