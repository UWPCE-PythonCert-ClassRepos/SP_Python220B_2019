'''
Inventory Module to update and append Invoice File.
'''
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, monthly_price):
    '''Create and append invoice file.'''

    with open(invoice_file, 'a') as csvfile:
        row_format = [customer_name, item_code,
                      item_description, str(monthly_price)
                     ]

        write_row = ','.join(row_format)
        csvfile.write(write_row)
        csvfile.write('\n')

def single_customer(customer_name, invoice_file):
    """This function returns a function to add new rental items to
       invoice file."""

    def add_customer(rental_items):

        with open(rental_items, 'r') as csvfile:
            new_item = partial(add_furniture, invoice_file, customer_name)
            reader = csv.reader(csvfile)

            for row in reader:
                item_code = row[0]
                item_description = row[1]
                monthly_price = row[2]
                new_item(item_code, item_description, monthly_price)

    return add_customer
