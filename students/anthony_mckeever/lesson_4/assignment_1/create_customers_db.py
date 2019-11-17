# Advanced Programming In Python - Lesson 4 Assigmnet 1: Iterators, Generators and Comprehensions
# RedMine Issue - SchoolOps-14
# Code Poet: Anthony McKeever
# Start Date: 11/13/2019
# End Date: 11/14/2019

"""
Creates the customer's database.
"""

import logging
import argparse

from itertools import islice

from peewee import SqliteDatabase
from peewee import IntegrityError
from peewee import OperationalError

from customer_db_schema import Customers

PARSER = argparse.ArgumentParser(description='Create Customers DB')
PARSER.add_argument('--debug', type=int, default=0,
                    help="Display errors in log.")
PARSER.add_argument('--import-file', type=str, default=None,
                    help="A CSV of customers to import.")
PARSER.add_argument('--import-bandwidth', type=int, default=5,
                    help="Max customers to hold in memory during import")


def set_logging(level):
    """
    Set up logging for the application.

    :level:     The level of log verbosity.
    """
    log_level = parse_log_level(level)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    msg = f"Logging set at level: {logging.getLevelName(log_level)}"
    logging.info(msg)


def parse_log_level(level):
    """
    Parses the logging level from the debug integer as set in the arguments.

    :level: The logging level to parse.
    """
    log_levels = {0: logging.INFO,
                  1: logging.ERROR,
                  2: logging.DEBUG}

    log_level = log_levels.get(level)

    if log_level is None:
        raise ValueError(f"Logging level {level} has no implementation.")

    return log_level


def init_database():
    """
    Initialize the database.
    """
    logging.info("Initializing database...")

    database = SqliteDatabase("customers.db")
    database.connect()
    database.execute_sql("PRAGMA foreign_keys = ON;")

    logging.info("Database initialized successfully.")

    return database


def create_tabels(database):
    """
    Creates tables in the database.

    :database:  The database to create tables in.
    """
    logging.info("Creating tables...")

    database.create_tables([Customers])
    logging.info("Tables created successfully.")


def import_customers(file, bandwidth):
    """
    Import customers from a file.

    :file:      The input CSV file.
    :bandwidth: The number of lines to hold in memory while writing customers.
    """
    with open(file, "r") as in_file:
        contents = list(islice(in_file, bandwidth))

        while len(contents) > 0:
            write_customers(contents)
            contents = list(islice(in_file, bandwidth))


def write_customers(customer_list):
    """
    Write a collection of customers to the database.

    :customer_list:     A list of CSV strings representing customers.
    """
    # Disable unnecessary-comprehension within this one method only.
    # pylint: disable=unnecessary-comprehension
    customers = [c for c in customer_generator(customer_list)]
    write_iterator(customers, write_to_db)


def write_iterator(customer_list, func):
    """
    Iterate through the list of customers and perform a desired operation.

    :customer_list:     A list of CSV strings representing customers.
    :func:              The function to perform on each iteration.
    """
    iterator = iter(customer_list)

    while True:
        try:
            customer = next(iterator)
        except StopIteration:
            break
        func(customer)


def write_to_db(customer):
    """
    Write a customer to the DB.

    This handles exceptions peewee.IntegrityError and peewee.OperationalError
    and writes them to the log when encountered.

    :customer:  The customer to write.
    """
    try:
        current = Customers.get_or_create(**customer)
        logging.info("Customer written successfully.")
        logging.debug(current)
    except (IntegrityError, OperationalError) as error:
        logging.info("Failed to write customer.")
        logging.error(error)
        logging.debug(customer)


def customer_generator(customer_list):
    """
    Yield return a customer as a dictionary from a list of comma delimited
    strings.
    """
    for customer in customer_list:
        customer = customer.split(',')
        yield {"customer_id": customer[0],
               "first_name": customer[1],
               "last_name": customer[2],
               "home_address": customer[3],
               "phone_number": customer[4],
               "email_address": customer[5],
               "status": customer[6],
               "credit_limit": customer[7]}


def main(args):
    """
    The main method of the application.

    :args:  The arguments from argparse
    """
    set_logging(args.debug)
    database = init_database()
    create_tabels(database)

    if args.import_file is not None:
        import_customers(args.import_file, args.import_bandwidth)


if __name__ == "__main__":
    ARGS = PARSER.parse_args()
    main(ARGS)
