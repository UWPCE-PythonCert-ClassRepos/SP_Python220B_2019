""" This keeps rental records in a .csv file """

import csv
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ This function adds to the .csv file one item/customer at a time """
    with open(invoice_file, mode='a', newline='') as wkg_file:
        writer = csv.writer(wkg_file, delimiter=',')
        new_list = [customer_name, item_code, item_description, item_monthly_price]
        writer.writerow(new_list)

def single_customer(invoice_file, customer_name):
    """ This creates a function to return multiple entries for the same customer """
    add_rent_line = partial(add_furniture, invoice_file, customer_name)
    def add_customer_invoice(rental_file):
        """ This function adds a record for each row in the input csv file """
        with open(rental_file, mode='r') as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                in_code = row[0]
                in_description = row[1]
                in_price = row[2]
                add_rent_line(in_code, in_description, in_price)
    return add_customer_invoice

if __name__ == "__main__":
    #Discreet adding of records
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)

    #Adding of multiple records from a single customer
    CREATE_INVOICE = single_customer("rented_items.csv", "Susan Wong")
    CREATE_INVOICE("test_items.csv")
