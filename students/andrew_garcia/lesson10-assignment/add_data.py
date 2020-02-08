""" Adding New Data into CSV File"""

import csv
import random


def new_data():
    """ Creates a random customer, product, and rental """
    with open('customers.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        number = random.sample(range(10), 4)
        uid = ''.join(map(str, number))

        name = 'Customer' + uid
        address = uid + ' 16th Way South'
        phone = '555-555-' + uid
        email = name + '@gmail.com'

        writer.writerow([uid, name, address, phone, email])
        customer_info = [uid, name, address, phone, email]

    with open('products.csv', 'a', newline='') as file:
        writer = csv.writer(file)

        number = random.sample(range(10), 2)
        uid = ''.join(map(str, number))

        description_choices = ['Blue', 'Red', 'Black', 'Yellow', 'Green', 'Pink', 'White']
        product_choices = ['Chair', 'Television', 'Lamp', 'Table', 'Sofa']
        quantity = random.randint(0, 15)

        writer.writerow([uid, random.choice(description_choices),
                         random.choice(product_choices), quantity])
        product_info = [uid, random.choice(description_choices), random.choice(product_choices),
                        quantity]

    with open('rentals.csv', 'a', newline='') as file:
        number = random.sample(range(10), 3)
        uid = ''.join(map(str, number))

        writer = csv.writer(file)
        writer.writerow([uid, product_info[0], customer_info[0], customer_info[1],
                         customer_info[2], customer_info[3], customer_info[4]])


def csv_first_line():
    """ Writes first line to csv to identify items """
    with open('products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['product_id', 'description', 'product_type', 'quantity_available'])

    with open('customers.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'name', 'address', 'phone_number', 'email'])

    with open('rentals.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['rental_id', 'product_id', 'user_id', 'name', 'address', 'phone_number',
                         'email'])


csv_first_line()
for i in range(100):
    new_data()
