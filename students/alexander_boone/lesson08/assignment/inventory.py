'''
Generate HP Norton Inventory CSV and add inventory data from file with
list of customer rentals.
'''
import csv
from functools import partial


def add_furniture(invoice_file, customer_name,
                  item_code, item_description,
                  item_monthly_price):
    '''Create/update inventory file with data provided.'''
    with open(invoice_file, 'a') as csvfile:
        write_list = [
            customer_name,
            item_code,
            item_description,
            str(item_monthly_price)
        ]
        write_string = ','.join(write_list)
        csvfile.write(write_string)
        csvfile.write('\n')


def single_customer(customer_name, invoice_file):
    '''
    Return function that requires one parameter(rentals file for
    one customer) and adds data from file to invoice_file.
    '''
    def single_customer_adder(rental_items):
        '''Adds data from rental_items to invoice file.'''
        adder = partial(
            add_furniture,
            invoice_file=invoice_file,
            customer_name=customer_name
        )
        with open(rental_items, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                adder(
                    item_code=row[0],
                    item_description=row[1],
                    item_monthly_price=row[2]
                    )
    return single_customer_adder
