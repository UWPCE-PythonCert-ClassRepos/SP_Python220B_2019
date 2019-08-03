
import csv
import pandas as pd
from functools import partial


def add_furniture(invoice_file, customer_name,
                  item_code, item_description,
                  item_monthly_price):
    """function to add a new line to csv file"""

    filename = invoice_file

    with open(filename, mode='a', newline='') as invoice_file:
        invoice_writer = csv.writer(invoice_file, delimiter=',', quotechar='"')

        try:
            invoice_writer.writerow([customer_name, item_code,
                                    item_description,
                                    item_monthly_price])
        except Exception as ex:
            print(ex)
            pass


def single_customer(customer_name, invoice_file):

    """function to add new line to csv file for a given customer
        using closure and currying"""

    def process_rental(rental_items):

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
