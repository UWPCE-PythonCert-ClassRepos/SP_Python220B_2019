# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 12:08:59 2019
Modified on Thu Aug 22 12:28:45 2019
@author: Florentin Popescu
"""
# generate csv files, customers & rentals
# ==================================

# imports
import csv
import random
import logging
import importlib
REC = importlib.import_module("records", package=None)

# ==================================

# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("loger active")
# ==================================


SUFFIX = ['th', 'st', 'nd', 'rd'] + ['th'] * 6
ADR_FORMATING = "%d %d%s %s, %s %d"
# ==================================


def phone_number():
    """ generate phone number that doesn't start with zero """
    return random.randint(100_000_0000, 1_000_000_0000)


def random_name():
    """ generate (first_name, last_name) tuple """
    first = list(REC.FIRST_NAME.values())
    last = list(REC.LAST_NAME.values())
    return random.choice(first), random.choice(last)


def random_domain():
    """ generate email """
    return random.choice(list(REC.DOMAIN.values()))


def random_item_type():
    """ generate description of the rental """
    item_type = list(REC.ITEM_CATEGORY.values())
    return random.choice(item_type)


def random_description():
    """ generate a random description of the product """
    description = list(REC.RENTAL_ITEM.values())
    return random.choice(description)


def person_email(full_name, domain):
    """ generate first_last@domain.com for each customer"""
    return f"{full_name[0]}_{full_name[1]}@{domain}.com"


def random_address():
    """ generate street address """
    house_number = random.randint(1, 10000)
    street_number = random.randint(1, 1000)
    street = random.choice(("St.", "Ave."))
    location = random.choice([(v, k) for k, v
                              in REC.STATE_CAPITAL.items()])
    zipcode = random.randint(10_000, 100_000)
    return ADR_FORMATING % (house_number,
                            street_number,
                            SUFFIX[street_number % 10],
                            street,
                            location[0] + ", " + location[1],
                            zipcode)


def random_customer(customer_id):
    """ generate customer with name, address, phone number and email """
    customer = dict()
    customer_name_tpl = random_name()
    customer['customer_id'] = f'user{customer_id:04d}'
    customer['first_name'], customer['last_name'] = customer_name_tpl
    customer['address'] = random_address()
    customer['phone'] = phone_number()
    customer['email'] = person_email(customer_name_tpl, random_domain())
    return customer


def random_product(item_id):
    """ generate product with id and random quantity """
    product = dict()
    product['product_id'] = f'prd{item_id:04d}'
    product['description'] = random_description()
    product['product_type'] = random_item_type()
    product['quantity_available'] = random.randint(0, 100)
    return product


def write_csv(data, filename):
    """ write data to named csv file """
    try:
        keys = data[0].keys()
    except IndexError as err:
        LOGGER.info("data cannot be empty")
        LOGGER.info("ERROR: %s", err)
    with open(filename, 'w', newline='') as output_file:
        try:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            output_file.flush()
            output_file.close()
        except UnboundLocalError as err:
            LOGGER.info("cannot write empty data into file")
            LOGGER.info("ERROR: %s", err)
# ==================================


if __name__ == "__main__":
    try:
        N = int(input("enter the number or records to generate in each file" +
                      " (positive, non-zero integer)\n"))
        LOGGER.info("files generated with %s records each", N)
    except (ValueError, IndexError) as err:
        LOGGER.info("ERROR: %s", err)
        LOGGER.info("please enter a positive, non-zero integer")

    # generate customers csv file
    CUSTOMERS = [random_customer(i) for i in range(N)]
    try:
        write_csv(CUSTOMERS, 'customers.csv')
    except (PermissionError, IOError) as err:
        LOGGER.info("Incorect path or file 'customers.csv' is open")
        LOGGER.info(err)

    # generate products csv file
    PRODUCTS = [random_product(i) for i in range(N)]
    try:
        write_csv(PRODUCTS, 'products.csv')
    except (PermissionError, IOError) as err:
        LOGGER.info("Incorect path or file 'products.csv' is open")
        LOGGER.info(err)

    # generate rentals csv file
    RENTALS = list()
    for i in range(N):
        rental = dict()
        rental['rental_id'] = f'rnt{i:05d}'
        rental['customer_id'] = random.choice(CUSTOMERS)['customer_id']
        rental['product_id'] = random.choice(PRODUCTS)['product_id']
        RENTALS.append(rental)
    try:
        write_csv(RENTALS, 'rentals.csv')
    except (PermissionError, IOError) as err:
        LOGGER.info("Incorect path or file 'rentals.csv' is open")
        LOGGER.info(err)
# ==================================
