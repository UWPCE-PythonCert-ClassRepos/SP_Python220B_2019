"""
This is a one-off program to create the product_data, customer_data, and rentals_data csv files
in a folder named 'csvs'. This program is otherwise useless once the data is created. I only made
this because I couldn't find any pre-generated csv files or formats were given.
"""

import os
import csv
import logging
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'csvs'))

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'create_csv.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

def write_csv():
    """This method writes the csv files to import for testing"""
    try:
        os.mkdir(os.path.join(os.path.dirname(__file__), 'csvs'))
    except OSError:
        print("Could not create directory")
    else:
        print("Successfully created the directory")

    LOGGER.debug("Establishing dictionaries for csv")
    product_data = expand_product_data()

    customer_data = expand_customer_data()

    rentals_data = expand_rentals_data()

    LOGGER.debug("Writing to .csv files")
    with open(os.path.join(os.path.dirname(__file__), 'csvs', 'product_data.csv'),
              'w') as products:
        product_fields = ['id', 'description', 'product_type', 'quantity_available']
        product_writer = csv.DictWriter(products, delimiter=',', lineterminator='\n',
                                        fieldnames=product_fields)
        product_writer.writeheader()
        for key, value in product_data.items():
            product_row = {'id': key}
            product_row.update(value)
            product_writer.writerow(product_row)

    with open(os.path.join(os.path.dirname(__file__), 'csvs', 'customer_data.csv'),
              'w') as customers:
        customer_fields = ['id', 'name', 'address', 'phone_number']
        customer_writer = csv.DictWriter(customers, delimiter=',', lineterminator='\n',
                                         fieldnames=customer_fields)
        customer_writer.writeheader()
        for key, value in customer_data.items():
            customer_row = {'id': key}
            customer_row.update(value)
            customer_writer.writerow(customer_row)

    with open(os.path.join(os.path.dirname(__file__), 'csvs', 'rentals_data.csv'),
              'w') as rentals:
        rentals_fields = ['id', 'name', 'rentals']
        rentals_writer = csv.DictWriter(rentals, delimiter=',', lineterminator='\n',
                                        fieldnames=rentals_fields)
        rentals_writer.writeheader()
        for key, value in rentals_data.items():
            rentals_row = {'id': key}
            value['rentals'] = ' '.join(value['rentals'])
            rentals_row.update(value)
            rentals_writer.writerow(rentals_row)

    LOGGER.debug("Writing complete")

def expand_product_data():
    """This method expands the product_data to 1000 records"""
    product_data = {'prd001': {'description': 'TV', 'product_type': 'livingroom',
                               'quantity_available': 3},
                    'prd002': {'description': 'Couch', 'product_type': 'livingroom',
                               'quantity_available': 1},
                    'prd003': {'description': 'Chair', 'product_type': 'livingroom',
                               'quantity_available': 0}}
    for number in range(4, 1000):
        key = 'prd{}'.format('0'*(3-len(str(number)))+str(number))
        product_data.setdefault(key, {'description': "something{}".format(str(number)),
                                      'product_type': "type{}".format(str(number)),
                                      'quantity_available': number})
    return product_data

def expand_customer_data():
    """This method expands the customer_data to 1000 records"""
    customer_data = {'cst001': {'name': 'Charlie', 'address': '123 Fleet Street',
                                'phone_number': '1231234123'},
                     'cst002': {'name': 'Andrey', 'address': '123 Jordan Street',
                                'phone_number': '4564564567'},
                     'cst003': {'name': 'Vijay', 'address': '123 Lake Street',
                                'phone_number': '7987897891'}}

    for number in range(4, 1000):
        key = 'cst{}'.format('0'*(3-len(str(number)))+str(number))
        customer_data.setdefault(key, {'name': "something{}".format(str(number)),
                                       'address': "somewhere{}".format(str(number)),
                                       'phone_number': str(number)})
    return customer_data

def expand_rentals_data():
    """This method expands the rentals_data to 1000 records"""
    rentals_data = {'cst001': {'name': 'Charlie', 'rentals': ['prd001', 'prd002']},
                    'cst002': {'name': 'Andrey', 'rentals': ['prd002', 'prd003']},
                    'cst003': {'name': 'Vijay', 'rentals': ['prd001', 'prd003']}}

    for number in range(4, 1000):
        key = 'cst{}'.format('0'*(3-len(str(number)))+str(number))
        rentals_data.setdefault(key, {'name': 'Vijay', 'rentals': ['prd001', 'prd003']})
    return rentals_data

if __name__ == '__main__':
    write_csv()
