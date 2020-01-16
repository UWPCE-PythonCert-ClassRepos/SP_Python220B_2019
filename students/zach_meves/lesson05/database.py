"""
database.py

Represent customer and product data in a MongoDB.

Lesson 05
Zach Meves
"""

import pymongo
import csv
import os

CLIENT = pymongo.MongoClient()
DB = CLIENT['hp_norton']

PRODUCTS = DB.products
CUSTOMERS = DB.customers
RENTALS = DB.rentals


def read_csv(file, keyed=False):
    """
    Read a CSV file and return the data as a list of dictionaries.

    :param file: str, file to read
    :param keyed: bool, True to return a dictionary keyed on the first-column
    values, False to return a list of dicts
    :return: list or dict
    """

    with open(file) as f:
        reader = csv.reader(f)
        header = [_.strip() for _ in next(reader)]

        output = []
        for line in reader:
            line_values = [_.strip() for _ in line]
            # Check if need to convert to floats or ints
            for i in range(len(line_values)):
                try:
                    line_values[i] = float(line_values[i])
                except ValueError:
                    pass

            output.append(dict(zip(header, line_values)))

    if keyed:  # Convert to a single dictionary keyed with the first column
        key = header[0]
        return dict(zip((entry[key] for entry in output), output))

    return output


def import_data(directory, products, customers, rentals):
    """
    Create and populate a new MongoDB instance with data from
    the provided files.

    :param directory: str, directory name of files
    :param products: str, name of file with product definitions
    :param customers: str, name of file with customer definitions
    :param rentals: str, name of file with rental information
    :returns: tuple, number of products, customers, and rentals added
    :returns: tuple, errors that occur for adding products, customers, and rentals
    """

    product_data = read_csv(os.path.join(directory, products))
    customer_data = read_csv(os.path.join(directory, customers))
    rental_data = read_csv(os.path.join(directory, rentals))

    res_prod = PRODUCTS.insert_many(product_data)
    res_cust = CUSTOMERS.insert_many(customer_data)
    res_rent = RENTALS.insert_many(rental_data)

    inserted_prods = len(res_prod.inserted_ids)
    inserted_custs = len(res_cust.inserted_ids)
    inserted_rents = len(res_rent.inserted_ids)

    return (inserted_prods, inserted_custs, inserted_rents), \
           (len(product_data) - inserted_prods, len(customer_data) - inserted_custs,
            len(rental_data) - inserted_rents)


def show_available_products():
    """
    Return products that are currently available in dictionary format.

    :return: dict
    """

    pass



def show_products_for_customer():
    """
    Return list of all available products.

    :return: list
    """

    pass


def show_rentals(product_id):
    """
    Return user information for customers who have rented the product.

    :param product_id: str, product ID
    :return: dict
    """

    output = {}

    results = RENTALS.find({"product_id": product_id})
    for rental in results:
        uid = rental['user_id']
        output[uid] = CUSTOMERS.find_one({"user_id": uid},
                                         projection={'_id': False, "user_id": False})

    return output

