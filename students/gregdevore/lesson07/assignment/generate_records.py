'''
Generate bogus customer, product, and rental records for testing
'''

import random
import string
import os
from uuid import uuid4

def generate_random_letters(length=5):
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])

def generate_random_numbers(length=3):
    return ''.join([random.choice(string.digits) for _ in range(length)])

def generate_customer():
    '''
    Generate random customer record of the form
    user_id,name,address,phone_number,email
    The user_id is the primary key, and must be unique
    '''
    user_id = str(uuid4())
    name = ' '.join([generate_random_letters() for _ in range(2)])
    address = generate_random_numbers() + ' ' + ' '.join([generate_random_letters() for _ in range(2)])
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
    return ','.join(list(map(str,[uuid4() for _ in range(3)])))

if __name__ == "__main__":
    folder = 'sample_csv_files'
    records = 1000

    print('Writing customer records...')
    with open(os.path.join(folder,'customers.csv'),'w') as customers:
        customers.write('user_id,name,address,phone_number,email\n')
        for _ in range(records):
            customers.write(generate_customer() + '\n')

    print('Writing product records...')
    with open(os.path.join(folder,'products.csv'),'w') as products:
        products.write('product_id,description,product_type,quantity_available\n')
        for _ in range(records):
            products.write(generate_product() + '\n')

    print('Writing rental records...')
    with open(os.path.join(folder,'rentals.csv'),'w') as rentals:
        rentals.write('rental_id,customer_id,product_id\n')
        for _ in range(records):
            rentals.write(generate_rental() + '\n')
