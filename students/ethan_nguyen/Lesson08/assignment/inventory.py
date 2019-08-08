""" module for inventory """
import csv
from functools import partial
import pandas as pd


def add_furniture(invoice_file, customer_name,
                  item_code, item_description,
                  item_monthly_price):

    """function to add a new line to csv file"""

    filename = invoice_file

    with open(filename, mode='a', newline='') as invoice:
        invoice_writer = csv.writer(invoice, delimiter=',', quotechar='"')

        try:
            invoice_writer.writerow([customer_name, item_code,
                                     item_description,
                                     item_monthly_price])
        except IOError as ex:
            print(ex)


def single_customer(customer_name, invoice_file):

    """function to add new line to csv file for a given customer
        using closure and currying"""

    def process_rental(rental_items):

        """function to add new line to csv file a give rental item"""

        input_df = pd.read_csv(rental_items, header=None)
        input_df.columns = ['code', 'description', 'price']

        add_invoice = partial(add_furniture,
                              invoice_file=invoice_file,
                              customer_name=customer_name)

        for _, row in input_df.iterrows():
            add_invoice(item_code=row['code'],
                        item_description=row['description'],
                        item_monthly_price=row['price'])

    return process_rental
