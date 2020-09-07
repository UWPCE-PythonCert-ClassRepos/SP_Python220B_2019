"""
Used to update inventory file to keep track of all
rental information.
"""
import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Adds a rental item to the inventory

    :param invoice_file: The name of the file where inventory is maintained
    :param customer_name: The customer name for the rental
    :param item_code: The item code for the item being rented
    :param item_description: The description of the item rented
    :param item_monthly_price: The monthly price of the rental
    """
    with open(invoice_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([customer_name, item_code, item_description, item_monthly_price])


def single_customer(customer_name, invoice_file):
    """
    Returns a create invoice method that will take in a list of furniture rented
    and update the invoice file with the renatl information
    :param customer_name: The name of the rental customer
    :param invoice_file: The name of the file to update
    """
    add_furn_for_cust = partial(add_furniture,
                                invoice_file=invoice_file,
                                customer_name=customer_name)

    def create_invoice(items_file):
        """
        Adds items from the items file to the invoice file,
        assoicating with the customer

        :param items_file: A list of items rented
        """
        with open(items_file, newline='') as input_file:
            field_names = ['item_code', 'item_description', 'item_monthly_price']
            reader = csv.DictReader(input_file, field_names)
            for row in reader:
                add_furn_for_cust(item_code=row['item_code'],
                                  item_description=row['item_description'],
                                  item_monthly_price=row['item_monthly_price'])
    return create_invoice
