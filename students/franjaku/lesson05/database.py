"""
    database.py
    Contains interactions for the HP Norton Mongodb database.

    Functionality:
        HP Norton customer: see a list of all products available for rent
        HP Norton salesperson: see a list of all of the different products, showing product ID,
            description, product type and quantity available.
        HP Norton salesperson: see a list of the names and contact details
            (address, phone number and email) of all customers who have rented a certain product.
"""
import logging
import csv
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
     This function takes a directory name three csv files as input, one with product data, one with
    customer data and the third one with rentals data and creates and populates a new MongoDB
    database with these data. It returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a count of any errors
    that occurred, in the same order.

    :return: tuple1, record count of the # of products, customers, rentals added
             tuple2, count of any errors that occurred, in the same order
    """
    # Open connection
    mongo = MongoDBConnection()

    with mongo:
        # Create connection to database
        db = mongo.connection.HPNortonDatabase

        # create/connect to collections
        product_data = db['product_data']
        customer_data = db['customer_data']
        rental_data = db['rental_data']

        # load product data
        with open(directory_name + '/' + product_file) as prod_file:
            reader = csv.DictReader(prod_file)
            data = []
            for row in reader:
                data.append({'product_id': row['product_id'],
                             'description': row['description'],
                             'product_type': row['product_type'],
                             'quantity_available': row['quantity_available']})
        product_data.insert_many(data)

        # load customer data
        with open(directory_name + '/' + customer_file) as cust_file:
            reader = csv.DictReader(cust_file)
            data = []
            for row in reader:
                data.append({'customer_id': row['customer_id'],
                             'name': row['name'],
                             'address': row['address'],
                             'phone_number': row['phone_number'],
                             'email': row['email']})

        customer_data.insert_many(data)

        # load rental data
        with open(directory_name + '/' + rentals_file) as rent_file:
            reader = csv.DictReader(rent_file)
            data = []
            for row in reader:
                data.apppend({'rental_id': row['rental_id'],
                              'customer_id': row['customer_id'],
                              'product_id': row['product_id']})

        product_data.insert_many(data)

    # Place holders
    tuple1 = ()
    tuple2 = ()
    return tuple1, tuple2


def show_available_products():
    """
    Returns a Python dictionary of products listed as available with the following fields:
        product_id
        description
        product_type
        quantity_available
    """
    pass


def show_rentals(product_id):
    """
    Returns a Python dictionary with the following user information from users that have rented
    products matching product_id:
        user_id
        name
        address
        phone_number
        email
    """
    pass


def main():
    directory_path = 'C:/Users/USer/Documents/UW_Python_Certificate/Course_2/' \
                     'SP_Python220B_2019/students/franjaku/lesson05/data_files'
    tup1, tup2 = import_data(directory_path, 'product_data.csv',
                                      'customer_data.csv', 'rental_data.csv')

    print(tup1)
    print(tup2)


if __name__ == "__main__":
    main()
