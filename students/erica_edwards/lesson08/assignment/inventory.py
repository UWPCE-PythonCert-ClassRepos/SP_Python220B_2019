"""Replace inventory spreadsheet"""
import csv
from os import path
from functools import partial

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """Add items to rental file"""
    if path.exists(invoice_file):
        mode = 'a'
    else:
        mode = 'w'
    with open(invoice_file, mode) as csv_file:
        csv_file.write(f'{customer_name},{item_code},{item_description},{item_monthly_price}\n')

def single_customer(output_file_name, customer_name):
    """"add furniture items to rented_items file for a single customer"""
    rentals = partial(add_furniture, output_file_name, customer_name)
    def create_invoice(input_file_name):
        with open(input_file_name, "r") as file:
            csv_reader = csv.reader(file, delimiter=',')
            for line in csv_reader:
                rentals(*line)
                # print(line)
    return create_invoice


if __name__ == "__main__":
    add_furniture('rented_items.csv', 'Elisa Miles', 'LR06', 'Sofa', 25)
    add_furniture('rented_items.csv', 'Edward Data', 'DR05', 'Kitchen Table', 12)
    add_furniture('rented_items.csv', 'Alex Gonzales', 'LR08', 'TV', 15)
    create_invoice = single_customer('rented_items.csv', 'Susan Wong')
    create_invoice('test_items.csv')
