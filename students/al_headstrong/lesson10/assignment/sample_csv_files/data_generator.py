"""
Module to generate 1,000,000 rows of data in csv file.
"""

import random
import csv
import string


DATA_FILES = ('customers_short.csv',
              'products_short.csv',
              'rentals_short.csv',
              'customers_long.csv',
              'products_long.csv',
              'rentals_short.csv')

MY_LIST_SHORT = list(range(1, 101))
MY_LIST_LONG = list(range(1, 100001))

FIRST_NAMES = ['Alan',
               'Beth',
               'Charlie',
               'Daphne',
               'Earl',
               'Frankie',
               'Greg',
               'Hannah',
               'Idris',
               'Jane',
               'Ken',
               'Letty',
               'Manny',
               'Nikki',
               'Orwell',
               'Persephone',
               'Quincy',
               'Ricki',
               'Starburns',
               'Trixie',
               'Uncle',
               'Verna',
               'Walker',
               'Xena',
               'Yannick',
               'Zoe']

LAST_NAMES = ['Hernandez',
              'Garcia',
              'Martinez',
              'Gonzalez',
              'Lopez',
              'Rodriguez',
              'Perez',
              'Sanchez',
              'Ramirez',
              'Flores',
              'Gomez',
              'Torres',
              'Diaz',
              'Vasquez',
              'Cruz',
              'Morales',
              'Gutierrez',
              'Reyes']

STREET_SUFFIXES = ['St','Ave','Pl', 'Dr', 'Rd']

PRODUCT_DESCRIPTIONS = ['80-inch TV stand',
                        '72-inch TV stand',
                        '60-inch TV stand',
                        '54-inch TV stand',
                        'L-shaped sofa',
                        'Sectional sofa',
                        'King size bed frame',
                        'Queen size bed frame',
                        'Double size bed frame',
                        'Single size bed frame',
                        'Table with leaves',
                        'Desk',
                        'Desk Light',
                        'Coffee Table',
                        'Throw Pillow']

PRODUCT_TYPES = ['livingroom',
                 'bedroom',
                 'diningroom',
                 'den',
                 'kitchen']

def generate_customer(my_list, data_file):
    with open(data_file, mode='w', newline='') as f:
        WRITER = csv.writer(f)
        WRITER.writerow(['customer_id', 'name', 'address', 'phone_number', 'email', 'credit_limit'])
        for i in my_list:
            WRITER.writerow(gen_customer_row(i))


def gen_customer_row(num):
    """Return list of data similar to existing csv."""
    return [f'user{num}',
            f'{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}',
            f'{random.randrange(1,10000)} {random.randrange(1,400)} {random.choice(STREET_SUFFIXES)}',
            f'{random.randrange(100,999)}-{random.randrange(100,999)}-{random.randrange(1000,9999)}',
            f'{"".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))}@u.edu',
            f'{100 * random.randrange(1,100)}']

def generate_products(my_list, data_file):
    with open(data_file, mode='w', newline='') as f:
        WRITER = csv.writer(f)
        WRITER.writerow(['product_id', 'description', 'product_type', 'quantity_available'])
        for i in my_list:
            WRITER.writerow(gen_product_row(i))


def gen_product_row(num):
    """Return list of data similar to existing csv."""
    return [f'prd{num}',
            f'{random.choice(PRODUCT_DESCRIPTIONS)}',
            f'{random.choice(PRODUCT_TYPES)}',
            f'{random.randrange(1,20)}']

def generate_rentals(my_list, data_file):
    with open(data_file, mode='w', newline='') as f:
        WRITER = csv.writer(f)
        WRITER.writerow(['rental_id', 'customer_id', 'product_id', 'quantity'])
        for i in my_list:
            WRITER.writerow(gen_rental_row(i))


def gen_rental_row(num):
    """Return list of data similar to existing csv."""
    return [f'r{num}',
            f'user{random.randrange(1,1000)}',
            f'prd{random.randrange(1,1000)}',
            f'{random.randrange(1,8)}']


generate_customer(MY_LIST_SHORT, 'customers_short.csv')
generate_products(MY_LIST_SHORT, 'products_short.csv')
generate_rentals(MY_LIST_SHORT, 'rentals_short.csv')
generate_customer(MY_LIST_LONG, 'customers_long.csv')
generate_products(MY_LIST_LONG, 'products_long.csv')
generate_rentals(MY_LIST_LONG, 'rentals_long.csv')