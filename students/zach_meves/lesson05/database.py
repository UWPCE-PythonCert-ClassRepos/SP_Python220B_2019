"""
database.py

Represent customer and product data in a MongoDB.

Lesson 05
Zach Meves
"""

import pymongo
import csv


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

    pass


def show_available_products():
    """
    Return products that are currently available in dictionary format.

    :return: dict
    """

    pass


def show_rentals(product_id):
    """
    Return user information for customers who have rented the product.

    :param product_id: str, product ID
    :return: dict
    """

    pass
