#!/usr/env/bin python3
"""
improved performance to analyze records
counting number per each years 2013-2018
counting the number of ao

"""

import datetime
import csv

DATE_INDEX = 5
AO_INDEX = 6


def get_year_and_ao(data: list) -> tuple:
    """return the year from date field and ao filed as tuple"""
    return data[DATE_INDEX][-4:], data[AO_INDEX]


def analyze(filename: str) -> tuple:
    """analyze the file for year counts and 'ao' records"""
    start = datetime.datetime.now()

    reader = csv.reader(open(filename, 'r'),
                        delimiter=',',
                        quotechar='"')

    found = 0
    year_count = {
        "2013": 0,
        "2014": 0,
        "2015": 0,
        "2016": 0,
        "2017": 0,
        "2018": 0,
    }

    for line in map(get_year_and_ao, reader):
        try:
            year_count[line[0]] += 1
        except KeyError:
            pass
        found += int("ao" in line[1])

    print(year_count)
    print(f"'ao' was found {found} times")
    end = datetime.datetime.now()

    return (start, end, year_count, found)

def main():
    """main"""
    filename = "\\".join(["C:",
                          "Users",
                          "pants",
                          "PycharmProjects",
                          "SP_Python220B_2019",
                          "students",
                          "tim_lurvey",
                          "lesson06",
                          "assignment",
                          "data",
                          "exercise.csv"])

    analyze(filename=filename)


if __name__ == "__main__":
    main()
