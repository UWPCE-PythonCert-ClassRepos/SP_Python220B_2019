"""
Create a function called add_furniture that takes the following input parameters:
This function will create invoice_file (to replace the spreadsheet’s data)
if it doesn’t exist or append a new line to it if it does.
After adding a few items to the same file,
the file created by add_furniture should look something like this:
"""
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    creates an invoice file if DNE or appends.
    """
    with open(invoice_file, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow((customer_name, item_code, item_description, float(item_monthly_price)))


def single_customer(invoice_file, customer_name):
    """iterates through the invoice file"""
    def rentals(data_file):
        with open(data_file, newline="") as file:
            new_row = partial(add_furniture, invoice_file, customer_name)
            data = csv.reader(file)
            for row in data:
                new_row(item_code=row[0],
                        item_description=row[1],
                        item_monthly_price=row[2])
    return rentals


if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    NEW_INVOICE = single_customer("rented_items.csv", "Susan Wong")
    NEW_INVOICE("data.csv")
