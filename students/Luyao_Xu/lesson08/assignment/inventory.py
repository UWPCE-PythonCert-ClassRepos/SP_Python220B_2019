"""
Functions to add furniture to csv
"""
import csv
from functools import partial


def add_furniture(invoice_file="", customer_name="", item_code="",
                  item_description="", item_monthly_price=""):
    """
    update master invoice file , create new cvs file if it does not exist
    :param invoice_file:
    :param customer_name:
    :param item_code:
    :param item_description:
    :param item_monthly_price:
    :return:None
    """

    with open(invoice_file, 'a+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([customer_name, item_code, item_description,
                         item_monthly_price])
        return (invoice_file, customer_name, item_code,
                item_description, item_monthly_price)


def single_customer(customer_name, invoice_file):
    """
    A function iterate through rental items and add each of
    them to the invoice file.
    :param invoice_file:
    :param customer_name:
    :return: A function that add item to invoice_file
    """
    def rentals_add(rental_items):
        with open(rental_items, 'r') as file:
            reader = csv.reader(file)
            add_item = partial(add_furniture, invoice_file=invoice_file,
                               customer_name=customer_name)
            for row in reader:
                add_item(item_code=row[0], item_description=row[1],
                         item_monthly_price=row[2])
    return rentals_add


def add_test():
    """Add test data to file"""
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa",
                  '25')
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table",
                  '10')
    add_furniture("rented_items.csv", "Alex Gonzales", "Queen Mattress", '17')


if __name__ == '__main__':
    add_test()
    CREATE_INVOICE = single_customer("Susan Wong", "invoice_file.csv")
    CREATE_INVOICE("test_items.csv")