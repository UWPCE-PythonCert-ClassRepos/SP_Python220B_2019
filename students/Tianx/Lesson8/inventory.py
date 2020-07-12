"""Python function that will create and update an inventory CSV file
with all the information that is currently entered through the spreadsheet program. """
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    """This function will create invoice_file if it doesn’t exist
    or append a new line to it if it does. """
    with open(invoice_file, 'a+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        customer_info = [customer_name, item_code, item_description, str(item_monthly_price)]
        writer.writerow(customer_info)


def single_customer(customer_name, invoice_file):
    """returns customer_rental function that takes 'rental_items' as a parameter"""
    def customer_rental(rental_items):
        """Closure to add single customer details"""
        with open(rental_items, 'r', newline='') as rentals:
            reader = csv.reader(rentals)
            add_invoice_items = partial(add_furniture, invoice_file, customer_name)
            for row in reader:
                add_invoice_items(item_code=row[0],
                                  item_description=row[1],
                                  item_monthly_price=row[2])
    return customer_rental
