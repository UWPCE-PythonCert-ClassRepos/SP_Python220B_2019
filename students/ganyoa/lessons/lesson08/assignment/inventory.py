'''
Advanced Programming in Python Lesson 8
Functional Techniques
'''

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    '''open csv file to input additional customer data'''

    with open(invoice_file, "a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([customer_name, item_code,
                             item_description, item_monthly_price])

def single_customer(customer_name, invoice_file):
    '''use coverage to call nested function new_rental from single customer'''

    #reads as add_function(invoice_file, customer_name, *args)
    add_items_partial = partial(add_furniture, invoice_file, customer_name)
    def new_rental(rental_items):
        with open(rental_items, "r") as input_file:
            input_reader = csv.reader(input_file)
            for row in input_reader:
                #adds these arguements to end of add_function above
                add_items_partial(row[0], row[1], row[2])
    return new_rental


if __name__ == '__main__':
    add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "BR02", "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")
