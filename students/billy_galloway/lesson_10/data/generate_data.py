'''
Generate a million entries
'''
from random import randrange
import random
import csv
import sys
sys.path.append("./data")


# def random_date():
#     ''' generates a random date '''
#     start = datetime.datetime.strptime("1/01/2013", '%m/%d/%Y')
#     end = datetime.datetime.strptime("12/31/2018", '%m/%d/%Y')
#     delta = end - start
#     output = start + timedelta(days=randrange(delta.days))

#     return output.strftime('%m/%d/%Y')

# def write_csv(filename):
#     ''' writes a csv file with a million lines of data '''
#     num_list = [11, 7]
#     with open(filename, 'w') as file:
#         # file.write(f'guid,count_0,count_1,count_2,count_3,date,ao\n')
#         for i in range(1000000):
#             number = random.choice(num_list)
#             if i % number == 0:
#                 file.write(f'{str(uuid.uuid1())},{i+1},{i+2},{i+3},{i+4},{random_date()},ao\n')
#             else:
#                 file.write(f'{str(uuid.uuid1())},{i+1},{i+2},{i+3},{i+4},{random_date()}\n')

def write_customer(filename):
    ''' write customer to csv file '''
    first_name_list = ['Adam', 'Andrew', 'Kate', 'Elisa', 'Maya', 'Will', 'John', 'Sarah']
    last_name_list = ['Smith', 'Jones', 'Adams', 'Harris', 'Miles', 'Data', 'Cruz']
    street_name_list = ['Railroad', 'Union', 'Broadway', 'Cactus', 'Elliot', 'Thomas']
    street_type_list = ['Avenue', 'Road', 'Drive', 'Street']

    with open(filename, 'w') as file:
        for i in range(1, 10000):
            first = random.choice(first_name_list)
            last = random.choice(last_name_list)
            name = f'{first} {last}'
            home_address = random.choice(street_name_list)
            street_type = random.choice(street_type_list)
            true_false = random.choice([True,False])
            file.write(f'user{i + 4:03d},{name},{i + 300:03d} {home_address} {street_type},{first.lower()}.{last.lower()}@hpnorton.com,555-555-{i:04d},{bool(true_false)},{i + 10000:05d}\n')


def write_product(filename):
    living_room = ['TV stand', 'L-shaped sofa','60-inch TV','40-inch TV']
    office = ['Desk lamp','Computer','Desk']
    kitchen = ['Refrigerator','Dishwasher', 'Toaster', 'Oven']
    laundry_room = ['Washing machine', 'Dryer', 'Vacuum']
    products = [living_room, office, kitchen, laundry_room]
    
    with open(filename, 'w') as file:
        for i in range(1, 10000):
            description = random.choice(products)
            quantity = randrange(0,10)
            if description is living_room:
                description = random.choice(description)
                file.write(f'prd{i + 5:03d},{description},livingroom,{quantity}\n')
            elif description is office:
                description = random.choice(description)
                file.write(f'prd{i + 5:03d},{description},office,{quantity}\n')
            elif description is kitchen:
                description = random.choice(description)
                file.write(f'prd{i + 5:03d},{description},kitchen,{quantity}\n')
            elif description is laundry_room:
                description = random.choice(description)
                file.write(f'prd{i + 5:03d},{description},laundry room,{quantity}\n')

def write_rentals(rentals, customer, product):
    with open(product) as file:
        product_id = []
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            lrow = list(row)
            if int(lrow[3]) != 0:
                product_id.append(lrow[0])
    with open(customer) as file:
        customer_id = []
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            lrow = list(row)
            if lrow[5] == 'True':
                customer_id.append(lrow[:5])
    with open(rentals, 'w') as file:
        for i in range(len(customer_id)):
            file.write(f'{product_id[i]},{",".join(customer_id[i])}\n')
        
    

write_customer('customer_large.csv')
write_product('product_large.csv')
write_rentals('rentals_large.csv', 'customer_large.csv', 'product_large.csv')