'''Module that expand records for database.py'''

import csv
import random

def expand_customers(customers_filename):
    '''Create more customer entries'''
    writer = csv.writer(customers_filename)
    writer.writerow(['c_id', 'name', 'address', 'phone_number', 'email'])

    num = 1
    for num in range(1001):
        entry = [(f'c{num:04}'), (f'John {num}'), (f'{num} street'),
                 (f'1-206-555-{num:04}'), (f'email{num}@gmail.com')]
        writer.writerow(entry)
        num += 1

def expand_products(products_filename):
    '''Create more product entries'''
    writer = csv.writer(products_filename)
    writer.writerow(['p_id', 'description', 'product_type', 'quantity_available'])

    list_1 = ['red', 'blue', 'green', 'yellow', 'black', 'white']
    list_2 = ['shiny', 'merry', 'strong', 'leather', 'crazy', 'chiffon']
    list_3 = ['pants', 'weapon', 'hat', 'bag', 'armor', 'helmet']
    list_4 = ['food', 'weapon', 'artifact']

    num = 1
    for num in range(1001):
        desc = (f'{random.choice(list_1)} {random.choice(list_2)} {random.choice(list_3)}')
        entry = [(f'p{num:04}'), desc, random.choice(list_4), random.randint(0, 16)]
        writer.writerow(entry)
        num += 1

def expand_rentals(rentals_filename):
    '''Create more rental entries'''
    writer = csv.writer(rentals_filename)
    writer.writerow(['r_id', 'p_id', 'c_id'])
    r_rand = random.randint(1, 1001)
    p_rand = random.randint(1, 1001)
    c_rand = random.randint(1, 1001)

    num = 1
    for num in range(1001):
        writer.writerow([(f'r{random.randint(1, 1001):04}'),
                         (f'p{random.randint(1, 1001):04}'), (f'c{random.randint(1, 1001):04}')])
        num += 1

with open('customers.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
    expand_customers(filename)

with open('products.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
    expand_products(filename)

with open('rentals.csv', mode='a', newline='', encoding='utf-8-sig') as filename:
    expand_rentals(filename)
