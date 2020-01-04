""" This module expands customer, product and rental data to 1000 rows """

import csv
import random 
import names
from faker import Faker
from datetime import timedelta
import pandas as pd

def expand_data(num_rows):
    """ Expands data to specified number of rows """
    prod_list = []
    cust_list = []
    rental_list = []

    fake = Faker()

    desc_list = ['TV', 'table', 'chair', 'bed', 'desk']
    prod_type = ['living room', 'bedroom', 'kitchen']

    for i in range(num_rows):
        user_id = f'user{str(i+1).zfill(5)}'
        prod_id = f'prd{str(i+1).zfill(5)}'
        first = names.get_first_name()
        last = names.get_last_name()
        rent_start = fake.date_between(start_date="-30y", end_date="today")
        rent_end  = rent_start + timedelta(days = random.randint(10,400))

        prod_list.append([prod_id, random.choice(desc_list), 
                          random.choice(prod_type), random.randint(0,20)])
        cust_list.append([user_id, f'{first} {last}', fake.street_address(), 
                          fake.phone_number()[:12], f'{first}.{last}@gmail.com'])
        rental_list.append([prod_id, user_id, rent_start, rent_end, random.randint(1,5)])

    return {'products':prod_list, 'customers': cust_list, 'rentals': rental_list}


if __name__ == '__main__':
    out_list = expand_data(1000)

    prod_df = pd.DataFrame(out_list['products'], 
                           columns=['id', 'description', 'product_type', 'quantity_available'])
    cust_df = pd.DataFrame(out_list['customers'], 
                           columns=['id', 'name', 'address', 'phone', 'email'])
    rent_df = pd.DataFrame(out_list['rentals'], 
                           columns=['productid', 'userid', 'rental_start', 'rental_end', 'items_rented'])

    prod_df.to_csv('products.csv', header=True, index=False)
    cust_df.to_csv('customers.csv', header=True, index=False)
    rent_df.to_csv('rentals.csv', header=True, index=False)
