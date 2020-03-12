'''
Generate a million entries
'''
from random import randrange
import random
import csv
import sys
sys.path.append("./data")


def random_date():
    ''' generates a random date '''
    start = datetime.datetime.strptime("1/01/2013", '%m/%d/%Y')
    end = datetime.datetime.strptime("12/31/2018", '%m/%d/%Y')
    delta = end - start
    output = start + timedelta(days=randrange(delta.days))

    return output.strftime('%m/%d/%Y')

def write_csv(filename):
    ''' writes a csv file with a million lines of data '''
    num_list = [11, 7]
    with open(filename, 'w') as file:
        # file.write(f'guid,count_0,count_1,count_2,count_3,date,ao\n')
        for i in range(1000000):
            number = random.choice(num_list)
            if i % number == 0:
                file.write(f'{str(uuid.uuid1())},{i+1},{i+2},{i+3},{i+4},{random_date()},ao\n')
            else:
                file.write(f'{str(uuid.uuid1())},{i+1},{i+2},{i+3},{i+4},{random_date()}\n')

def write_customer(filename):
    ''' write customer to csv file '''
    first_name_list = ['Adam', 'Andrew', 'Kate', 'Elisa', 'Maya', 'Will', 'John', 'Sarah']
    last_name_list = ['Smith', 'Jones', 'Adams', 'Harris', 'Miles', 'Data', 'Cruz']
    street_name_list = ['Railroad', 'Union', 'Broadway', 'Cactus', 'Elliot', 'Thomas']
    street_type_list = ['Avenue', 'Road', 'Drive', 'Street']
    
    with open(filename, 'a') as file:
        for i in range(1, 997):
            first = random.choice(first_name_list)
            last = random.choice(last_name_list)
            home_address = random.choice(street_name_list)
            street_type = random.choice(street_type_list)

            file.write(f'user{i + 4:03d},{first} {last},{i:03d} {home_address} {street_type},{first.lower()}.{last.lower()}@hpnorton.com,555-555-{i:04d},{i + 10000:05d}\n')

def write_product(filename):
    pass

def write_rentals(filename):
    pass


write_customer('customer.csv')