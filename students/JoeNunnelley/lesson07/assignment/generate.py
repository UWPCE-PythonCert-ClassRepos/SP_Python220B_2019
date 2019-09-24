#! /usr/bin/env python3
"""
Dynamically generate data for lesson 07
"""
import csv
import datetime
from random import choice, randint
from string import ascii_uppercase
import sys


def phn():
    """ Function to formulate a phone number """
    phone = '0000000000'
    while '9' in phone[3:6] or phone[3:6] == '000' \
            or phone[6] == phone[7] == phone[8] == phone[9]:
        phone = str(randint(10**9, 10**10-1))

    return phone[:3] + '-' + phone[3:6] + '-' + phone[6:]


def write(filename, header, contents):
    """ Write the file """
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for _, val in contents.items():
            writer.writerow(val)

    csv_file.close()


def generate_customers(number=10):
    """
    ID, NAME, ADDRESS, PHONE_NUMBER, EMAIL
    user001, "Elisa Miles", "4490 Union Street", "206-922-0882", "eli.m@y.com"
    user002, "Maya Data", "4936 Elliot Avenue", "206-777-1927", "mdata@uw.edu"
    """
    header = ["ID", "NAME", "ADDRESS", "PHONE_NUMBER", "EMAIL"]
    contents = {}
    for i in range(number):
        customer_id = 'user_{:0>10}'.format(i)
        name = ''.join(choice(ascii_uppercase) for i in range(32))
        address = ''.join(choice(ascii_uppercase) for i in range(128))
        phone_number = phn()
        email = "{}.domain.com".format(customer_id)
        contents[customer_id] = [customer_id, name, address, phone_number, email]

    write('customers.csv', header, contents)


def generate_products(number=10):
    """
    ID, DESCRIPTION, PRODUCT_TYPE, QUANTITY_AVAILABLE
    "prd001", "60-inch TV", "livingroom", 3
    "prd002", "L-Shaped Sofa", "livingroom", 1
    """
    header = ['ID', 'DESCRIPTION', 'PRODUCT_TYPE', 'QUANTITY_AVAILABLE']
    contents = {}
    for i in range(number):
        product_id = 'product_{:0>10}'.format(i)
        description = ''.join(choice(ascii_uppercase) for i in range(32))
        product_type = 'type_{:0>10}'.format(i)
        quantity = str(randint(0, 1000))
        contents[product_id] = [product_id, description, product_type, quantity]

    write('products.csv', header, contents)


def generate_rentals(number=10):
    """
    ID, CUSTOMER_ID, PRODUCT_ID, RENTAL_START_DATE, RENTAL_END_DATE
    1, user001, prd001, 2018-12-22, 2018-12-23
    2, user001, prd002, 2018-12-22, 2018-12-24
    """
    header = ['ID', 'CUSTOMER_ID', 'PRODUCT_ID',
              'RENTAL_START_DATE', 'RENTAL_END_DATE']
    contents = {}
    rental_frequency = randint(0, 5)
    print('Generating : {} rentals'.format(number * rental_frequency))
    for i in range(number * rental_frequency):
        rental_id = 'rental_{:0>10}'.format(i)
        customer_id = str(randint(0, number))
        product_id = str(randint(0, number))
        rental_start = datetime.date(randint(2007, 2013),
                                     randint(1, 12),
                                     randint(1, 28))
        rental_end = datetime.date(randint(2014, 2019),
                                   randint(1, 12),
                                   randint(1, 28))
        contents[rental_id] = [rental_id, customer_id, product_id,
                               rental_start, rental_end]

    write('rentals.csv', header, contents)


def main(entrycount):
    """ The main function caller """
    generate_customers(int(entrycount))
    generate_products(int(entrycount))
    generate_rentals(int(entrycount))


if __name__ == "__main__":
    main(sys.argv[1])
