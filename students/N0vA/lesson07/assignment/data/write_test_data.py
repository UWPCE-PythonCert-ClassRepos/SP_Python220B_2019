"""
Module to write test data for lesson07 assignment.
"""

import random
import names
from faker import Faker

def write_product_data():
    """Writes product test data file."""

    # Setup data
    headers = ['product_id', 'description', 'product_type', 
               'quantity_available']
    
    with open('product_data.csv', 'w') as csvfile:
        column_names = ','.join(headers)
        csvfile.write(column_names)
        csvfile.write('\n')
        
        products = ['chair', 'tv', 'bed', 'table',
                     'espressomachine', 'computer',
                     'sofa']
        
        product_dict = {'chair': 'office',
                     'tv': 'livingroom',
                     'bed': 'bedroom',
                     'table': 'diningroom',
                     'espressomachine': 'kitchen',
                     'computer': 'office',
                     'sofa': 'livingroom'
                    }
        
        for i in range(1001):
            random_product = random.choice(products)
            row_format = [str(random.randint(0, 10001)),
                          random_product,
                          product_dict[random_product],
                          random.choice([str(i) for i in range(6)])]
            write_row = ','.join(row_format)
            csvfile.write(write_row)
            csvfile.write('\n')


def write_customer_data():
    """Write customer test data."""
    # Set up Faker for addresses and phone numbers

    fake = Faker('en_US')
    
    headers = ['user_id', 'name', 'address',
               'phone_number', 'email']
    
    with open('customer_data.csv', 'w') as csvfile:
        column_names = ','.join(headers)
        csvfile.write(column_names)
        csvfile.write('\n')
        
        for i in range(1001):
            row_format = [str(random.randint(0, 1000000)),
                          names.get_full_name(),
                          (fake.address()).replace('\n', ' ').replace(',', ''),
                          fake.phone_number(),
                          fake.email()]

            write_row = ','.join(row_format)
            csvfile.write(write_row)
            csvfile.write('\n')

def write_rental_data():
    """Write rentals test data."""

    headers = ['product_id', 'user_id']

    with open('rental_data.csv', 'w') as csvfile:
        column_names = ','.join(headers)
        csvfile.write(column_names)
        csvfile.write('\n')
        
        for i in range(1001):
            row_format = [str(random.randint(0, 10001)),
                          str(random.randint(0, 1000000))]
            write_row = ','.join(row_format)
            csvfile.write(write_row)
            csvfile.write('\n')

if __name__ == "__main__":
    # Write test data.

    write_product_data()
    write_customer_data()
    write_rental_data()