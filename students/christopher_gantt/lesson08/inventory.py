'''inventory.py'''
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    '''adds a furniture rental to the invoice file of your choice'''
    with open(invoice_file, 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow([customer_name]+
                            [item_code]+
                            [item_description]+
                            [item_monthly_price])

def single_customer(customer_name, invoice_file):
    '''
        using the customer name and the invoice file you want to
        write to, this function uses the function defined within
        to take rental items stored in a csv file and write them
        to your invoice file
    '''
    def function(rental_items):
        with open(rental_items) as csvfile:
            spamreader = csv.reader(csvfile)
            add_rental_items = partial(add_furniture,
                                       invoice_file=invoice_file,
                                       customer_name=customer_name)
            for row in spamreader:
                add_rental_items(item_code=row[0],
                                 item_description=row[1],
                                 item_monthly_price=row[2])
    return function
