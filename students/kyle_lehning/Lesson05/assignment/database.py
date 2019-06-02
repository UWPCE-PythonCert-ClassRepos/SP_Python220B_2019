#!/usr/bin/env python3
"""Migration of product data from csv into MongoDB"""
from pymongo import MongoClient


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host='192.168.0.24', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


MONGO = MongoDBConnection()


def main():
    pass


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    This function takes a directory name and three csv files as input, one with product data,
    one with customer data, and the third one with rentals data. It creates and populates a new
    MongoDB database with these data. It returns 2 tuples: the first with a record count of the
    number of products, customers, and rentals added (in that order), the second with a count
    of any errors that occurred, in the same order
    """
    with MONGO:
        # mongodb database; it all starts here
        db = MONGO.connection.media
    pass


def show_available_products():
    """
    Returns a python dictionary of products listed as available with the following fields:
    product_id
    description
    product_type
    quantity_available
    """
    pass


def show_rentals(product_id):
    """
    This function returns a python dictionary with the following user information from users that
    have rented products matching product_id:
    user_id
    name
    address
    phone_number
    email
    """
    pass


if __name__ == "__main__":
    main()
