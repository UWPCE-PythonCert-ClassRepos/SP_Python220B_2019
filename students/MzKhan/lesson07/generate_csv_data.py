"""
This module generates three files.
customers.csv - This file contains the customer data.
products.csv - This file contains the product data.
rentals.csv - This file contains the rental data
"""

import csv
import random
from os import path
from datetime import date, timedelta


def generate_random_date():
    """Returns a date in the mm/dd/yyyy format"""
    start_date = date(2012, 1, 1)
    end_date = date.today()
    max_days = (end_date - start_date).days
    new_date = start_date + timedelta(days=random.randrange(0, max_days))
    new_date = new_date.strftime('%m/%d/%Y')
    return new_date


def generate_customers_data(number_of_rows=100000):
    """write the customer data to a csv file."""
    with open(path.join('data', 'customers.csv'), 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in range(number_of_rows):
            user = 'user{:0>10d}'.format(row)
            name = 'name{:0>10d}'.format(row)
            address = 'address{:0>10d}'.format(row)
            phone = 'phone{:0>10d}'.format(row)
            email = 'email{:0>10d}'.format(row)
            writer.writerow([user, name, address, phone, email])


def generate_products_data(number_of_rows=100000):
    """write the products data to the file."""
    with open(path.join('data', 'products.csv'), 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in range(number_of_rows):
            product = 'product{:0>10d}'.format(row)
            description = 'description{:0>10d}'.format(row)
            category = 'category{:0>10d}'.format(row)
            quantity = random.randrange(0, 10)
            writer.writerow([product, description, category, quantity])


def generate_rentals_data(number_of_rows=100000):
    """write the rentals data to the file."""
    with open(path.join('data', 'rentals.csv'), 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in range(number_of_rows):
            date_one = generate_random_date()
            date_two = generate_random_date()
            if date_one[-4:] < date_two[-4:]:
                start_date = date_one
                end_date = date_two
            else:
                start_date = date_two
                end_date = date_one
            product = 'product{:0>10d}'.format(row)
            user = 'user{:0>10d}'.format(row)
            category = 'category{:0>10d}'.format(row)
            quantity = random.randrange(0, 10)
            writer.writerow([product, user, category, start_date, end_date,
                             quantity])


if __name__ == "__main__":

    generate_customers_data()
    generate_products_data()
    generate_rentals_data()
