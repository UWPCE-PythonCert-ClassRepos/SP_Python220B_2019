'''
HP Norton Inventory System Version 8
'''
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''Add furntiture to invoice.'''
    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([customer_name, item_code,
                         item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    '''Add rentals for specific customer to invoice_file.'''
    add_furn = partial(add_furniture, invoice_file, customer_name)

    def return_function(rental_items):
        with open(rental_items) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                item_code = row[0]
                item_description = row[1]
                item_monthly_price = row[2]
                add_furn(item_code, item_description, item_monthly_price)
    return return_function
