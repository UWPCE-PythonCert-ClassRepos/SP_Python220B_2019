#!/usr/bin/env python3
"""Extend existing csv"""

import random
import datetime
import string
import csv


def random_date():
    """Return a random date from 1/1/2010 to 12/31/2018"""
    start_date = datetime.date(2010, 1, 1)
    date_range = datetime.timedelta(random.randint(0, 3286))
    date = start_date + date_range
    return date.strftime("%m/%d/%Y")


def random_ao():
    """Randomly return either ao or ''"""
    if bool(random.getrandbits(1)):
        return "ao"
    else:
        return ""


def random_str(num):
    """return a random string of letters and numbers of length num"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=num))


def list_increase(num_list):
    """Return a list that has had each item increased by 1"""
    return [x+1 for x in num_list]


def main():
    """Add 999,990 lines to exercise.csv"""
    extend_range = 999990
    num_list = [10, 11, 12, 13]
    with open('exercise.csv', 'a') as fd:
        for n in range(extend_range):
            unique_line = "{}-{}-{}-{}-{}".format(
                random_str(8), random_str(4), random_str(4), random_str(4), random_str(12))
            num_list = list_increase(num_list)
            num_string = ','.join(map(str, num_list))
            rand_date = random_date()
            ao = random_ao()
            full_line = "\n{},{},{},{}".format(
                unique_line, num_string, rand_date, ao)
            fd.write(full_line)


if __name__ == '__main__':
    main()
