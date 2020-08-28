# Stella Kim
# Assignment 7: Concurrency & Async

"""
Create CSV files each with one thousand data records following
Assignment #5 data format.
"""

import random
import csv
from timeit import timeit as timer
from faker import Faker
FAKE = Faker()


def generate_customers(default=1000):
    """Generate rows of customer data using Assignment 5 formatting"""
    with open('./data/customers.csv', 'w', newline='') as file:
        data_file = csv.writer(file, quoting=csv.QUOTE_NONE)
        columns = 'user_id', 'name', 'address', 'phone_number', 'email'
        data_file.writerow(columns)
        for i in range(default):
            first_name = FAKE.first_name()
            last_name = FAKE.last_name()
            address = FAKE.street_address()
            email = (f'{last_name}.{first_name}@example.com').lower()
            prefix = random.choice(['206555', '425555', '360555', '509555'])
            phone = ''.join(['{}'.format(random.randint(0, 9))
                             for num in range(0, 4)])
            row = f'user{i+1:04}', first_name + ' ' + last_name, address,\
                  prefix + phone, email
            data_file.writerow(row)


def generate_products(default=1000):
    """Generate rows of product data using Assignment 5 formatting"""
    prod_appliance = ['Toaster', 'Blender', 'Vacuum Cleaner',
                      'Rice Cooker', 'Drill', 'Oven']
    prod_furniture = ['Bookshelf', 'Office Chair', 'Couch', 'Desk',
                      'Table', 'Dresser']
    with open('./data/products.csv', 'w', newline='') as file:
        data_file = csv.writer(file, quoting=csv.QUOTE_NONE)
        items = prod_appliance + prod_furniture
        columns = 'product_id', 'description', 'product_type',\
                  'quantity_available'
        data_file.writerow(columns)
        for i in range(default):
            item = random.choice(items)
            color = (FAKE.safe_color_name()).title()
            prod_type = 'Appliance' if item in prod_appliance else 'Furniture'
            quantity = random.randint(0, 25)
            row = f'prd{i+1:04}', color + ' ' + item, prod_type, quantity
            data_file.writerow(row)


def generate_rentals(default=1000):
    """Generate rows of rentals data using Assignment 5 formatting"""
    with open('./data/rentals.csv', 'w', newline='') as file:
        data_file = csv.writer(file, quoting=csv.QUOTE_NONE)
        columns = 'product_id', 'user_id'
        data_file.writerow(columns)
        for _i in range(default):
            row = f'prd{random.randint(0, 1000):04}',\
                  f'user{random.randint(0, 1000):04}'
            data_file.writerow(row)


def _code_timer():
    """Measure time it takes to run code"""
    print(timer('generate_data()', globals=globals(), number=1))


if __name__ == "__main__":
    generate_customers(10)
    generate_products(10)
    generate_rentals(10)
    # _code_timer()
