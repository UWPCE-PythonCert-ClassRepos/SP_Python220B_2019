'''
spent alot of time figuring out
"InvalidDocument: documents must have only string keys, key was None"
--had commas in the address
'''
import random
from faker import Faker
fake = Faker()


def gen_address():
    address = fake.address().split('\n')[0]
    return str(address.replace(',', ''))


def gen_email(name):
    prov = ['gmail.com', 'hotmail.com', 'aol.com', 'uw.edu', 'buttmail.gov']
    name = name.replace(' ', '')
    return f'{name}@{random.choice(prov)}'


def gen_celly():
    return f'({random.randint(100, 999)})-{random.randint(100, 999)}-{random.randint(1000, 9999)}'


def expand_customers_file():
    '''Do the work'''
    filename = 'csv_files/customers.csv'
    with open(filename, 'w') as out_file:
        lines = 1
        out_file.write('customer_id,name,address,phone_number,email')
        while lines < 1000:
            cust_name = fake.name()
            data_string = f'\nuser{lines:03d},{cust_name},{gen_address()},{gen_celly()},{gen_email(cust_name)}'
            # print(data_string)
            out_file.write(str(data_string))
            lines += 1


def expand_products_file():
    '''Do the work'''
    # product_id,description,product_type,quantity_available
    # prd001,60-inch TV stand,livingroom,3
    product_type = ['junk', 'trash', 'booboo', 'sweat-meats', 'waters']

    filename = 'csv_files/products.csv'
    with open(filename, 'w') as out_file:
        lines = 1
        out_file.write('product_id,description,product_type,quantity_available')
        while lines < (1e3):
            data_string = f'\nprd{lines:03d},{" ".join(fake.words(nb=3))},{random.choice(product_type)},{random.randint(0, 999)}'
            # print(data_string)
            out_file.write(data_string)
            lines += 1


def expand_rentals_file():
    '''Do the work'''
    # product_id,description,product_type,quantity_available
    # prd001,60-inch TV stand,livingroom,3

    filename = 'csv_files/rentals.csv'
    with open(filename, 'w') as out_file:
        lines = 1
        out_file.write('rental_id,customer_id,product_id,quantity')
        while lines < (1e3):
            data_string = f'\nr{lines:03d},user{random.randint(1, 999)},prd{random.randint(1, 999)},{random.randint(1, 999)}'
            # print(data_string)
            out_file.write(data_string)
            lines += 1


if __name__ == "__main__":
    expand_customers_file()
    expand_products_file()
    expand_rentals_file()
