"""
Functions to create and update the inventory file
"""
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    Create, and subsequently update a CSV file that lists which furniture is rented
    to which customer
    """
    with open(invoice_file, mode='a', newline='') as file_object:
        invoice_writer = csv.writer(file_object, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
        invoice_writer.writerow([customer_name, item_code, item_description,
                                 "{:.2f}".format(item_monthly_price)])


def single_customer(customer_name, invoice_file):
    """ Load individual customers rentals """
    def load_customer(source_file):
        add_customer = partial(add_furniture, invoice_file, customer_name)
        try:
            with open(source_file, 'r') as customer_file:
                customer_reader = csv.reader(customer_file, delimiter=',')
                for row in customer_reader:
                    add_customer(row[0], row[1], float(row[2]))
        except FileNotFoundError:
            print(f"File {invoice_file} not found")

    return load_customer


if __name__ == '__main__':
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("test_items.csv")
