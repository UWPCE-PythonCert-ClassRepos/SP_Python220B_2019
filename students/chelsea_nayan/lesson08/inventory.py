'''A module to create and update an inventory CSV file using closures and currying'''
# Create and update a CSV dile that lsits which furniture is rented to which customer
# Create functionalities that will load individual customers rentals

import csv
from functools import partial

def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):
    '''Create invoice_file if it doesn't exist or append a new line to add in furniture'''
    with open(invoice_file, mode='a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([customer_name,
                         item_code,
                         item_description,
                         item_monthly_price])

# Need to use functools.partial and closures
# Add all items in a source file to the overall inventory under a single customer name
def single_customer(customer_name, invoice_file):
    '''Iterate through rental_items and add each item to invoice_file'''
    def single_rentals(rental_items):
        try:
            with open(rental_items, mode='r', newline='') as file:
                reader = csv.reader(file)

                # partial(): return a new partial object
                # https://docs.python.org/2/library/functools.html
                add_row = partial(add_furniture,
                                  customer_name=customer_name, # Fixed
                                  invoice_file=invoice_file) # Fixed
                for row in reader:
                    add_row(item_code=row[0], # Fixed
                            item_description=row[1], # Fixed
                            item_monthly_price=row[2]) # Fixed
        except FileNotFoundError:
            print('The file was not found.')

    return single_rentals

if __name__ == '__main__':
    # add_furniture('rented_items.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25.01)
    # add_furniture('rented_items.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10.00)
    # add_furniture('rented_items.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17.00)

    CREATE_INVOICE = single_customer('Susan Wong', 'rented_items_susan.csv')
    CREATE_INVOICE('test_items.csv')
