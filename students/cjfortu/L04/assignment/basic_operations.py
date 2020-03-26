#!/usr/bin/env python
"""
Main module for all program operations.

Run this module to run the program.

Loading the existing databse is in the load_databse module.
"""

import sys
from customer_model import *


def main_menu():
    """
    Provie the user with an input interface.

    Call functions based on the user's input.
    """

    valid_prompts = ['1', '2', '3', '4', '5', '6', 'q']
    user_prompt = None

    LOGGER.info("Function '6' now available.")
    while user_prompt not in valid_prompts:
        print("""Please choose from the following:
              '1' - Add a new customer
              '2' - Search a customer
              '3' - Delete a customer
              '4' - Update customer credit
              '5' - List active customers
              '6' - Display all customers
              'q' - Quit""")
        user_prompt = input(": ")

    if user_prompt == '1':
        print("Please provide the following customer information:")
        customer_id = input("customer ID (format is 'xxyyyy' where 'x' is an uppercase letter, "
                            "and 'y' is a digit): ")
        name = input('first name: ')
        last_name = input('last name: ')
        home_address = input('home address: ')
        phone_number = input('phone number (10 digits): ')
        email_address = input('email address: ')
        status = input("status ('active' or 'inactive'): ")
        credit_limit = input('credit limit (digits only): ')
        add_customer(customer_id, name, last_name, home_address, phone_number, email_address,
                     status, credit_limit)

    if user_prompt == '2':
        customer_id = input("Please provide the customer ID (format is 'xxyyyy' where 'x' is an "
                            "uppercase letter, and 'y' is a digit): ")
        search_customer(customer_id)

    if user_prompt == '3':
        customer_id = input("Please provide the customer ID (format is 'xxyyyy' where 'x' is an "
                            "uppercase letter, and 'y' is a digit): ")
        delete_customer(customer_id)

    if user_prompt == '4':
        customer_id = input("Please provide the customer ID (format is 'xxyyyy' where 'x' is an "
                            "uppercase letter, and 'y' is a digit): ")
        credit_limit = input("Please provide the new credit limit (digits only): ")
        update_customer_credit(customer_id, credit_limit)

    if user_prompt == '5':
        list_active_customers()

    if user_prompt == '6':
        display_all_customers()

    if user_prompt == 'q':
        exit_program()


def add_customer(*args):
    """
    Add a customer.

    args[0] = customer_id
    args[1] = name
    args[2] = last_name
    args[3] = home_address
    args[4] = phone_number
    args[5] = email_address
    args[6] = status
    args[7] = credit_limit
    """
    LOGGER.info('Adding customers')

    try:
        new_customer = Customer.create(
            customer_id=args[0],
            name=args[1],
            last_name=args[2],
            home_address=args[3],
            phone_number=args[4],
            email_address=args[5],
            status=args[6],
            credit_limit=args[7])
        new_customer.save()
        LOGGER.info(f'Database add successful {args[0]}')

    except Exception as exc:
        LOGGER.info(f'Error creating = {args[0]}')
        LOGGER.info(exc)


def search_customer(customer_id):
    """
    Search a customer based on customer ID.

    Return a dictionary object with name, last name, email address, phone number, and credit limit
    as keys.

    If no customer is found, then return an empty dictionary object.
    """
    LOGGER.info('Searching customers')

    try:
        searched_customer = Customer.get(Customer.customer_id == customer_id)
        returned_customer = {'name': searched_customer.name,
                             'last_name': searched_customer.last_name,
                             'email_address': searched_customer.email_address,
                             'phone_number': searched_customer.phone_number,
                             'credit_limit': searched_customer.credit_limit}
        LOGGER.info(f'dict object created for {customer_id}')

    except Exception as exc:
        LOGGER.info(f'{customer_id} not found')
        LOGGER.info(exc)
        LOGGER.info('Creating empty dict')
        returned_customer = {}

    finally:
        print(returned_customer)

    return returned_customer


def delete_customer(customer_id):
    """
    Delete a customer based on customer ID.
    """
    LOGGER.info('Deleting customers')

    try:
        Customer.get(Customer.customer_id == customer_id).delete_instance()
        LOGGER.info(f'{customer_id} deleted.')

    except Exception as exc:
        LOGGER.info(f'{customer_id} not found')
        LOGGER.info(exc)
        LOGGER.info('database unchanged')


def update_customer_credit(customer_id, credit_limit):
    """
    Delete a customer based on customer ID.
    """
    LOGGER.info('Updating customer credit')

    try:
        updated_customer = Customer.get(Customer.customer_id == customer_id)

    except Exception as exc:
        LOGGER.info(f'{customer_id} not found')
        LOGGER.info(exc)
        LOGGER.info('database unchanged')
        raise ValueError(f'{customer_id} not found')

    else:
        try:
            updated_customer.credit_limit = credit_limit
            updated_customer.save()
            LOGGER.info(f'{customer_id} credit limit updated.')
        except Exception:
            LOGGER.info(f'credit limit entry must be digits only')
            LOGGER.info('database unchanged')


def list_active_customers():
    """
    Delete a customer based on customer ID.
    """
    LOGGER.info('Listing number of active and inactive customers')

    try:
        active_customers = Customer.select().where(Customer.status == 'active').count()
        inactive_customers = Customer.select().where(Customer.status == 'inactive').count()
        LOGGER.info(f' active customers = {active_customers}')
        LOGGER.info(f' inactive customers = {inactive_customers}')

    except Exception as exc:
        LOGGER.info(exc)

    finally:
        active_inactive_count = (active_customers, inactive_customers)
        print('(active_customers, inactive_customers) = {}'.format(active_inactive_count))

    return active_inactive_count


def display_all_customers():
    """
    List all customers and their info using a GENERATOR COMPREHESION.

    A tuple of strings is returned.

    Each string is printed.
    """
    LOGGER.info('Listing all customers and their information using a GENERATOR COMPREHENSION.')

    entries = ((" {:<7}|{:^10}|{:^10}|{:<40}|{:^12}|{:>20}|{:^10}|{:^7}".
                format(customer.customer_id, customer.name, customer.last_name,
                       customer.home_address, customer.phone_number, customer.email_address,
                       customer.status, customer.credit_limit)) for customer in Customer)

    for entry in entries:
        print(entry)

    return entries


def exit_program():
    """
    Close the database and exit the program.
    """
    database.close()
    sys.exit()


if __name__ == '__main__':
    database = SqliteDatabase('customers.db')
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')

    while True:
        main_menu()
        input("Press Enter to continue.....")
