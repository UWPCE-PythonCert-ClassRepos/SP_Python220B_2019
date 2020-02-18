"""
Functionality to allow inventory management for HP Norton.
"""

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Add a new record to the CSV invoice_file in this format:

    customer_name,item_code,item_description,item_monthly_price
    """
    with open(invoice_file, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        writer.writerow([customer_name, item_code, item_description,
                         '{:.2f}'.format(float(item_monthly_price))])


def single_customer(customer_name, invoice_file):
    """
    Returns a function that will iterate through a file defined by rental_items and add
    them to the master inventory file, invoice_file, as rented to customer_name.
    """
    def import_from(rental_items):
        """
        Iterate through rental_items and add the discovered records to nonlocal invoice_file.
        Append nonlocal customer_name.
        """
        nonlocal customer_name
        nonlocal invoice_file

        import_record = partial(add_furniture, invoice_file=invoice_file,
                                customer_name=customer_name)

        with open(rental_items, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                import_record(item_code=row[0], item_description=row[1], item_monthly_price=row[2])

    return import_from
