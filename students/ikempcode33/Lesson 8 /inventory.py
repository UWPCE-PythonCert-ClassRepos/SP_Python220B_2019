"""inventory puts rental records in a rented_items csv file"""
import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """writes to a .csv file one item at a time with each of the descriptors"""
    with open(invoice_file, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        new_list = [customer_name, item_code, item_description, item_monthly_price]
        writer.writerow(new_list)


def single_customer(customer_name, invoice_file):
    """returns a function to add new rental items to invoice file using currying"""
    def add_customer(rental_items):
        with open(rental_items, 'r') as rental_csvfile:
            new_item = partial(add_furniture, invoice_file, customer_name)
            reader = csv.reader(rental_csvfile)

            for row in reader:
                item_code = row[0]
                description = row[1]
                price = row[2]
                new_item(item_code, description, price)
    return add_customer

if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    create_invoice = single_customer("rented_items.csv", "Susan Wong")
    create_invoice("test_items.csv")