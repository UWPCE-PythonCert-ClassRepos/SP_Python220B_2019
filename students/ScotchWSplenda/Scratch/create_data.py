'''for creating fake stuff'''

import uuid
import random
from _datetime import date, timedelta
from faker import Faker

fake = Faker()


def gen_guid():
    '''https://stackoverflow.com/questions/2257441/random-string-
    generation-with-upper-case-letters-and-digits/2257449
    How do I know these are unique?
    uuid.uuid4().hex.upper()[0:6] is prettier but doesnt match'''
    return uuid.uuid4()


def gen_date():
    '''Generate random date'''
    # based on the lowest date in poor_perf
    start = date(2010, 1, 1)
# datetime.date.today()
    end = date(2018, 12, 31)

    span = (end - start).days
    ran = random.randint(0, span)
    ran_date = (start + timedelta(days=ran)).strftime("%m/%d/%Y")
    return ran_date


def gen_address():
    address = fake.address().split('\n')[0]
    return str(address.replace(',', ''))


def gen_email(name):
    prov = ['gmail.com', 'hotmail.com', 'aol.com', 'uw.edu', 'buttmail.gov']
    name = name.replace(' ', '')
    return f'{name}@{random.choice(prov)}'


def gen_celly():
    return f'({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}'


def create_customers():
    header = 'customer_id,name,address,phone_number,email'
    with open('customers.csv', 'w') as workit:
        workit.write(header)
        for line in range(0, 10000):
            cust_name = fake.name()
            row = f'\n{"user{0:03}".format(line+1)},{cust_name},{gen_address()},{gen_celly()},{gen_email(cust_name)}'
            workit.write(row)
            line += 1


def create_products():
    header = 'product_id,description,product_type,quantity_available'
    product_type = ['junk', 'trash', 'booboo', 'sweat-meats', 'waters']
    with open('products.csv', 'w') as workit:
        workit.write(header)
        for line in range(0, 10000):
            row = f'\n{"prd{0:03}".format(line+1)},{" ".join(fake.words(nb=3))},{random.choice(product_type)},{random.randint(0, 999)}'
            workit.write(row)
            line += 1


def create_rentals():
    '''Do the work'''
    header = 'rental_id,customer_id,product_id,quantity'
    with open('rentals.csv', 'w') as workit:
        workit.write(header)
        for line in range(0, 10000):
            row = f'\n{"r{0:04}".format(line+1)},user{random.randint(1, 999)},prd{random.randint(1, 999)},{random.randint(1, 99)}'
            workit.write(row)
            line += 1


if __name__ == "__main__":
    create_customers()
    create_products()
    create_rentals()
