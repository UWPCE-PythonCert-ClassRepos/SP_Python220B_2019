# Advanced Programming in Python -- Lesson 5 Assignment 1
# Jason Virtue
# Start Date 2/20/2020

#Supress pylint warnings here
# pylint: disable=unused-wildcard-import,wildcard-import,invalid-name,too-few-public-methods,wrong-import-order,singleton-comparison,too-many-arguments,logging-format-interpolation

import csv

def main():
    customer_dict = []

    with open('customers.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            customer_dict.append(line)

    product_dict = []

    with open('products.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            product_dict.append(line)

    rental_dict = []

    with open('rentals.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            rental_dict.append(line)

    print(customer_dict)
    print(product_dict)
    print(rental_dict)

if __name__ == "__main__":
    main()
