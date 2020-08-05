'''
add_furniture("rented_items.csv", "Alex Gonzales", "Queen Mattress", 17)
create_invoice = single_customer("Susan Wong", "rented_items.csv")
create_invoice("test_items.csv")

->removed the 'invoice_file.csv' since it's repetitive
line 33 ; if row: #why the hell do I have to add this!>!>!?!> otherwise i got a
"IndexError: list index out of range"
'''
import csv
from functools import partial


def add_furniture(customer_name, item_code, item_description,
                  item_price):
    '''removed the 'invoice_file' arg since it's repetitive'''
    with open('invoice_file.csv',  mode='a+', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([customer_name, item_code, item_description, item_price])


def single_customer(customer_name):
    '''take a separate file and merge it into the main invoice file'''
    # create single_customer as object
    # partial(function name, fixed arguments...)
    add_furn = partial(add_furniture, customer_name=customer_name)

    def single_customer_return(customer_rental_file):
        '''second function is object(file to import)'''
        with open(customer_rental_file, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row: #why the hell do I have to add this!>!>!?!>
                    add_furn(item_code=row[0], item_description=row[1], item_price=row[2])
    return single_customer_return
