"""Module for creating csv files"""

import csv
import random
from datetime import date


def rand_date():
    """Generate random date from 1/01/2010 to today"""
    start_date = date(2010, 1, 1)
    end_date = date.today()
    random_date = start_date + ((end_date - start_date) * random.random())
    return random_date.strftime('%m/%d/%Y')


def create_products_data():
    """Create products.csv"""
    with open("sample_csv_files/products.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in range(1000):
            product_id = "product_id{}".format(row+1)
            description = "description{}".format(row+1)
            product_type = "product_type{}".format(row+1)
            quantity_available = random.randrange(0, 10)
            row_entry = [product_id, description, product_type,
                         quantity_available]
            writer.writerow(row_entry)


def create_customers_data():
    """Create customers.csv"""
    with open("sample_csv_files/customers.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in range(1000):
            customer_id = "customer_id{}".format(row+1)
            name = "name{}".format(row+1)
            address = "address{}".format(row+1)
            phone_number = "phone_number{}".format(row+1)
            email = "email{}".format(row+1)
            row_entry = [customer_id, name, address, phone_number, email]
            writer.writerow(row_entry)


def create_rentals_data():
    """Create rentals.csv"""
    with open("sample_csv_files/rentals.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in range(1000):
            rental_id = "r_id{}".format(random.randint(0, 1000))
            product_id = "p_id{}".format(random.randint(0, 1000))
            customer_id = "c_id{}".format(random.randint(0, 1000))
            row_entry = [rental_id, product_id, customer_id]
            writer.writerow(row_entry)


if __name__ == "__main__":
    create_products_data()
    create_customers_data()
    create_rentals_data()

