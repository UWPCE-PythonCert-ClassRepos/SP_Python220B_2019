"""
database.py

Represent customer and product data in a MongoDB.

Lesson 05
Zach Meves
"""

import pymongo
import csv


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
