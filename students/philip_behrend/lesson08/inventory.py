""" This module tracks furniture rentals using currying and closures """
import csv

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ This function adds data to file or creates file if it doesn't already exist """
    cust_list = [customer_name, item_code, item_description, item_monthly_price]
    with open(invoice_file, 'a', newline='') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(cust_list)

def single_customer(customer_name='John', invoice_file='test_invoice.csv'):
    """ Add customer with closure """
    rental_list = []
    def add_items(rental_file):
        """ Read in test rental file """
        with open(rental_file, 'r') as f:
            rd = csv.reader(f, quoting=csv.QUOTE_ALL)
            for row in rd:
                rental_list.append(row)

        for item in rental_list:
            add_furniture(invoice_file, customer_name, item[0], item[1], item[2])
    return add_items
