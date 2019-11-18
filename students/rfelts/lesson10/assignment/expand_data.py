#!/usr/bin/env python3

# Russell Felts
# Assignment 10

""" Expand data in csv files """

import csv
import random
import string


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def expand_products():
    """ Append data to the product file """
    with open('csv_files/products.csv', 'a') as data_file:
        # data_file.write("\n")
        data_writer = csv.writer(data_file)
        for i in range(5, 100):
            data_writer.writerow([i+1, random_string(10), random_string(5), 10])


def expand_customers():
    """ Append data to the product file """
    with open('csv_files/customers.csv', 'a') as data_file:
        # data_file.write("\n")
        data_writer = csv.writer(data_file)
        for i in range(4, 100):
            data_writer.writerow([i+1, random_string(10), random_string(5),
                                  "555-555-5555", "email.net"])


def main():
    """ Main """
    expand_products()
    expand_customers()


if __name__ == '__main__':
    main()
