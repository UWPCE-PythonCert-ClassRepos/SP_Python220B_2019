#!/usr/bin/env python3

# Russell Felts
# Assignment 7

""" Expand data in csv file to one million records """

# pylint: disable=too-many-arguments

import csv
import random


def main():
    """
    Append  rows to a csv file.
    """
    with open('csv_files/products.csv', 'a') as data_file:
        # Move to the next line before appending new row to the file
        data_file.write("\n")
        data_writer = csv.writer(data_file)
        for i in range(5, 10000):
            data_writer.writerow([str(i+1), " description{}".format(str(i)),
                                  " type{}".format(str(i)),
                                  " {}".format(str(random.randint(1, 100)))])

    with open('csv_files/customers.csv', 'a') as data_file:
        # Move to the next line before appending new row to the file
        data_file.write("\n")
        data_writer = csv.writer(data_file)
        for i in range(5, 10000):
            data_writer.writerow([str(i+1), " first_name{}".format(str(i)),
                                  " last_name{}".format(str(i)),
                                  " address{}".format(str(i)),
                                  " phone_number{}".format(str(i)),
                                  " email{}".format(str(i))])
if __name__ == '__main__':
    main()
