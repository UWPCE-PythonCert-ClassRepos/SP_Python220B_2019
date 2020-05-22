'''Module to generate dataset.'''
from faker import Faker
import random

fake = Faker()

# customer_id,name,address,phone_number,email,credit_limit
# user001,Alan Shepard,854 3rd St,206-395-9034,alshep@hotmail.com,100


def gen_address():
    address = fake.address().split('\n')[0]
    if ',' in address:
        address.replace(',', '')
    return address


def gen_email(name):
    prov = ['gmail', 'hotmail', 'aol', 'python', 'uw',
            'hpnorton', 'galaxy', 'universe', 'football']
    domain = ['edu', 'com', 'org', 'gov', 'co', 'net']

    name = name.replace(' ','')
    return f'{name}@{random.choice(prov)}.{random.choice(domain)}'

def gen_credit():
    ran = random.randint(3, 6)
    ran2 = random.randint(1, 9)
    return (10 ** ran) * ran2

def expand_file():
    '''Do the work'''
    filename = 'data/customers2.csv'
    with open(filename, 'a') as out_file:
        lines = 1
        out_file.write('customer_id,name,address,phone_number,email,credit_limit')
        while lines < (1e3):
            cust_name = fake.name()
            data_string = f'\nuser{lines:03d},{cust_name},{gen_address()},{fake.phone_number()},{gen_email(cust_name)},{gen_credit()}'
            # print(data_string)
            out_file.write(data_string)
            lines += 1

def expand_products_file():
    '''Do the work'''
    # product_id,description,product_type,quantity_available
    # prd001,60-inch TV stand,livingroom,3

    filename = 'data/products2.csv'
    with open(filename, 'a') as out_file:
        lines = 1
        out_file.write('product_id,description,product_type,quantity_available')
        while lines < (1e3):
            data_string = f'\nprd{lines:03d},{" ".join(fake.words(nb=3))},{fake.word()},{random.randint(0,1000)}'
            # print(data_string)
            out_file.write(data_string)
            lines += 1


if __name__ == "__main__":
    # expand_file()
    expand_products_file()
