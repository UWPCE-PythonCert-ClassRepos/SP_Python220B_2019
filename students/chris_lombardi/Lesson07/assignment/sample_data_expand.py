"""
A module to expand records in a dataset for testing.
"""

import csv
import os
import random

PATH = ('C:\\users\\chris\\documents\\PY220_Git\\SP_Python220B_2019\\students'
        '\\chris_lombardi\\Lesson07\\assignment\\data')
EMAILS = ['@aol.com', '@yahoo.com', '@msn.com', '@gmail.com']

def expand_products(filename, num_entries, directory=PATH):
    """Create additional product records and record in a *.csv file"""
    file_path = os.path.join(directory, filename)
    prod_id_count = 1
    prods = {'desk': 'office', 'table': 'dining_room', 'painting': 'living_room',
             'lamp': 'living_room', 'shovel': 'yard', 'shed': 'yard', 'chair': 'dining_room',
             'ladder': 'yard', 'lawnmower': 'yard', 'shears': 'yard', 'sofa': 'living_room',
             'rug': 'living_room'}

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['_id', 'description', 'product_type', 'quantity_available'])
            while prod_id_count <= num_entries:
                if prod_id_count < 10:
                    prefix = '000'
                elif prod_id_count < 100:
                    prefix = '00'
                elif prod_id_count < 1000:
                    prefix = '0'
                else:
                    prefix = ''

                id_build = ['prod', prefix, str(prod_id_count)]

                prod = random.choice(list(prods.keys()))
                row = [''.join(id_build), prod, prods.get(prod), random.randint(0, 100)]
                writer.writerow(row)
                prod_id_count += 1

    except FileNotFoundError:
        print('File Not Found')

def expand_customers(filename, num_entries, directory=PATH):
    """Create additional customer records in a *.csv file"""
    file_path = os.path.join(directory, filename)
    cust_id_count = 1
    first_names = {'John': 0, 'Pat': 0, 'Chris': 0, 'Josh': 0, 'Cary': 0, 'Sue': 0,
                   'Tom': 0, 'Carly': 0, 'Lisa': 0, 'George': 0, 'Megan': 0,
                   'Mark': 0, 'Scott': 0, 'Carey': 0, 'Jordan': 0}
    last_names = ['Anderson', 'Smith', 'Williams', 'Brown', 'Miller', 'Davis',
                  'Lincoln', 'Garfield', 'Washington', 'Madison', 'Johnson']

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['_id', 'name', 'address', 'phone_number', 'email'])
            while cust_id_count <= num_entries:
                if cust_id_count < 10:
                    prefix = '000'
                elif cust_id_count < 100:
                    prefix = '00'
                elif cust_id_count < 1000:
                    prefix = '0'
                else:
                    prefix = ''

                buildup = ['cust', prefix, str(cust_id_count)]
                name = random.choice(list(first_names.keys()))
                full_name = ' '.join([name, random.choice(last_names)])
                first_names[name] += 1

                # Generate random 10 digit phone number.
                digits = [str(random.randint(0, 9)) for digit in range(0, 9)]
                digits.insert(0, str(random.randint(1,9)))

                row = [''.join(buildup), full_name, gen_rand_address(),
                       ''.join(digits), ''.join([name, str(first_names.get(name)),
                       random.choice(EMAILS)])]
                writer.writerow(row)
                cust_id_count += 1
    except FileNotFoundError:
        print('File Not Found')

def gen_rand_address():
    """
    Generate a random address using various parameters.
    """

    street_suffix = {'0': 'th', '1': 'st', '2': 'nd', '3': 'rd', '4': 'th', '5': 'th', '6': 'th',
                     '7': 'th', '8': 'th', '9':'th', '10': 'th', '11': 'th', '12': 'th',
                     '13': 'th', '14': 'th', '15': 'th', '16': 'th', '17': 'th',
                     '18': 'th', '19': 'th'}
    street_opts = ['Rd.', 'St.', 'Ave.', 'Blvd.', 'Cir.', 'Dr.', 'Ln.', 'Pky.', 'Pl.', 'Way']

    house_num = str(random.randint(1, 9999))
    street_num = str(random.randint(1, 200))
    if street_num in street_suffix.keys():
        street_num += street_suffix.get(street_num)
    else:
        try:
            test_num = street_num[-1:]
            find_suf = str(street_suffix.get(test_num))
            street_num += find_suf
        except KeyError:
            street_num += 'th'

    street_type = random.choice(street_opts)
    address = [house_num, street_num, street_type]
    return ' '.join(address)

if __name__ == '__main__':
    PROD_FILE = 'products.csv'
    CUST_FILE = 'customers.csv'
    REPITITIONS = 1000
    expand_products(filename=PROD_FILE, num_entries=REPITITIONS, directory=PATH)
    expand_customers(filename=CUST_FILE, num_entries=REPITITIONS, directory=PATH)
