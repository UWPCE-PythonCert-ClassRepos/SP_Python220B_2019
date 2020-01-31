"""Module for creating csv files"""

import csv
import random
import os
from datetime import date


def rand_date():
    """Generate random date from 1/01/2010 to today"""
    start_date = date(2010, 1, 1)
    end_date = date.today()
    random_date = start_date + ((end_date - start_date) * random.random())
    return random_date.strftime('%m/%d/%Y')

def create_products_data():
    """"""
    with open("sample_csv_files/products.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in range(10000):
            row_entry = [product_id,
                         description,
                         product_type,
                         quantity_available]
            writer.writerow(row_entry)


def create_customers_data():
    """"""
    with open("sample_csv_files/customers.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in range(10000):
            cus
            
            row_entry = [customer_id,
                         name,
                         address,
                         phone_number,
                         email]
            writer.writerow(row_entry)


def create_rentals_data():
    """"""
    with open("sample_csv_files/rentals.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in range(10000):
            row_entry = [rental_id,
                         product_id,
                         customer_id]
            writer.writerow(row_entry)


if __name__ == "__main__":
    create_products_data()
    create_customers_data()
    create_rentals_data()