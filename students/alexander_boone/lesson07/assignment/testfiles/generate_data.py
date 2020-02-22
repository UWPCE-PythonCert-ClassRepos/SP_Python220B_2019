'''
This module generates 1000 lines of customer, product,
and rental data for linear and parallel processing.
'''
import time
import random
from faker import Faker

def generate_prod_data():
    '''Generate 1000 lines of product data.'''
    headers = ['product_id', 'description',
               'product_type', 'quantity_available']
    with open('prod_file_new.csv', 'w') as csvfile:
        headers_string = ','.join(headers)
        csvfile.write(headers_string)
        csvfile.write('\n')
        desc_list = [
            'chair',
            'tv',
            'bed',
            'table',
            'coffee table',
            'dresser',
            'mattress'
            ]
        prod_dict = {
            'chair':'livingroom',
            'tv':'livingroom',
            'bed':'bedroom',
            'table':'diningroom',
            'coffee table':'livingroom',
            'dresser':'bedroom',
            'mattress':'bedroom'
        }
        for i in range(1000):
            rand_choice = random.choice(desc_list)
            write_list = [
                f'prd{i:04d}',
                rand_choice,
                prod_dict[rand_choice],
                random.choice([str(i) for i in range(6)])
            ]
            write_string = ','.join(write_list)
            csvfile.write(write_string)
            csvfile.write('\n')

def generate_rental_data():
    '''Generate 1000 lines of rental data.'''
    headers = ['product_id', 'user_id']
    with open('rental_file_new.csv', 'w') as csvfile:
        headers_string = ','.join(headers)
        csvfile.write(headers_string)
        csvfile.write('\n')
        prd_list = [f'prd{i:04d}' for i in range(1, 1001)]
        user_list = [f'user{i:04d}' for i in range(1, 1001)]
        for _ in range(1000):
            write_list = [
                random.choice(prd_list),
                random.choice(user_list)]
            write_string = ','.join(write_list)
            csvfile.write(write_string)
            csvfile.write('\n')

def generate_cust_data():
    '''Generate 1000 lines of customer data.'''
    headers = ['user_id', 'name', 'address',
               'phone_number', 'email']
    fake = Faker('en_US')
    with open('cust_file_new.csv', 'w') as csvfile:
        headers_string = ','.join(headers)
        csvfile.write(headers_string)
        csvfile.write('\n')
        for i in range(1000):
            write_list = [
                f'user{i:04d}',
                fake.name(),
                (fake.address()).replace('\n', ' ').replace(',', ''),
                fake.phone_number(),
                fake.email()
            ]
            write_string = ','.join(write_list)
            csvfile.write(write_string)
            csvfile.write('\n')

START_TIME = time.time()

generate_prod_data()
generate_rental_data()
generate_cust_data()

RUNTIME = time.time() - START_TIME

# print('Total time for code generation: ' + str(RUNTIME))
