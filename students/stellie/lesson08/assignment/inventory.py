# Stella Kim
# Assignment 8: Functional Techniques

"""
Create program to create and update a CSV file.  Additionally, create
functionality to load individual customers rentals.
"""


def add_furniture(invoice_file, customer_name, item_code, item_description,
                  item_monthly_price):

    # This function will create invoice_file (to replace the spreadsheet’s
    # data) if it doesn’t exist or append a new line to it if it does. After
    # adding a few items to the same file, the file created by add_furniture
    # should look something like this:

    # Elisa Miles,LR04,Leather Sofa,25.00
    # Edward Data,KT78,Kitchen Table,10.00
    # Alex Gonzales,BR02,Queen Mattress,17.00

    # You can create a starter file in this format for testing, or you can
    # have your add function do it.


def single_customer(customer_name, invoice_file):
    # Output: Returns a function that takes one parameter, rental_items.

    # single_customer needs to use functools.partial and closures, in order
    # to return a function that will iterate through rental_items and add
    # each item to invoice_file.
