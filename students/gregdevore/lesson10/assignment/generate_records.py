'''
Generate bogus customer, product, and rental RECORDS for testing
'''

import random
import string
import os
from uuid import uuid4

def generate_random_letters(length=5):
    '''
    Generate a random string of ascii letters

    Args:
        length (int):
            Length of random string (default=5)
    Returns:
        Random string of specified length
    '''
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])

def generate_random_numbers(length=3):
    '''
    Generate a random string of digits

    Args:
        length (int):
            Length of random string (default=3)
    Returns:
        Random string of specified length
    '''
    return ''.join([random.choice(string.digits) for _ in range(length)])

def generate_customer():
    '''
    Generate random customer record of the form
    user_id,name,address,phone_number,email
    The user_id is the primary key, and must be unique
    '''
    user_id = str(uuid4())
    name = ' '.join([generate_random_letters() for _ in range(2)])
    address = generate_random_numbers() + ' ' + \
                ' '.join([generate_random_letters() for _ in range(2)])
    phone_number = '-'.join([generate_random_numbers(3) for _ in range(3)])
    email = '@'.join([generate_random_letters() for _ in range(2)]) + '.com'
    return ','.join([user_id, name, address, phone_number, email])

def generate_product():
    '''
    Generate random product record of the form
    product_id,description,product_type,quantity_available
    The product_id is the primary key, and must be unique
    '''
    product_id = str(uuid4())
    description = ' '.join([generate_random_letters() for _ in range(2)])
    product_type = generate_random_letters(7)
    quantity_available = str(random.randrange(10))
    return ','.join([product_id, description, product_type, quantity_available])

def generate_rental():
    '''
    Generate random rental record of the form
    rental_id,customer_id,product_id
    The rental_id is the primary key, and must be unique
    '''
    return ','.join(list(map(str, [uuid4() for _ in range(3)])))

if __name__ == "__main__":
    RECORDS = 10
    FOLDER = 'sample_csv_files_{:d}'.format(RECORDS)
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)

    print('Writing customer RECORDS...')
    with open(os.path.join(FOLDER, 'customers.csv'), 'w') as customers:
        customers.write('user_id,name,address,phone_number,email\n')
        for _ in range(RECORDS):
            customers.write(generate_customer() + '\n')

    print('Writing product RECORDS...')
    with open(os.path.join(FOLDER, 'products.csv'), 'w') as products:
        products.write('product_id,description,product_type,quantity_available\n')
        for _ in range(RECORDS):
            products.write(generate_product() + '\n')

    print('Writing rental RECORDS...')
    with open(os.path.join(FOLDER, 'rentals.csv'), 'w') as rentals:
        rentals.write('rental_id,customer_id,product_id\n')
        for _ in range(RECORDS):
            rentals.write(generate_rental() + '\n')
