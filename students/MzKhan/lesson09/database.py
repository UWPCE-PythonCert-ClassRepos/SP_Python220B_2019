"""
Work with the MongoDB database with python.
"""

import csv
import os
from pymongo import MongoClient

#pylint: disable = W0702, R0914

class MongoDatabase:
    """This class sets up the MongoDB database connection."""
    def __init__(self, host='127.0.0.1', port=27017):
        """constructor
        :parm host: local MongoDB host
        :parm port: local MongoDB port
        """
        self.host = host
        self.port = port
        self.connection = None
        self.database = None
        self.products = None
        self.customers = None
        self.rentals = None


    def __enter__(self):
        """
        This megic method is called in the background when a context manager
        is created.
        :return: self
        """
        self.connection = MongoClient(self.host, self.port)
        self.database = self.connection["HPNorton"]
        self.products = self.database["Product"]
        self.customers = self.database["Customer"]
        self.rentals = self.database["Rentals"]
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
         Close the database connection on exit.
        :parm exc_type:
        :parm exc_val:
        :parm:exc_tb
        """
        self.connection.close()


def drop_tables(mongo):
    """Drop the tables in the HPNorton database"""
    with mongo:
        mongo.products.drop()
        mongo.customers.drop()
        mongo.rentals.drop()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    import the data from the csv files.
    :parm dictionary_name:
    :parm product_file:
    :parm customer_file:
    :parm rentals_file:
    :return tuple:
    """
    product_err = 0
    customer_err = 0
    rental_err = 0

    product_count = 0
    customer_count = 0
    rental_count = 0

    mongo = MongoDatabase()
    drop_tables(mongo)
    with mongo:
        try:
            with open(os.path.join(directory_name, product_file)) as csv_file:
                product_data = csv.reader(csv_file, delimiter=",")
                for line in product_data:
                    new_product = {'product_id':line[0], 'description':line[1],
                                   'product_type':line[2],
                                   'quantity_available':line[3]}
                    mongo.products.insert_one(new_product)
                    product_count += 1
        except (FileNotFoundError, KeyError, IndexError):
            product_err += 1

        try:
            with open(os.path.join(directory_name, customer_file)) as csv_file:
                customer_data = csv.reader(csv_file, delimiter=",")
                for line in customer_data:
                    new_customer = {'customer_id':line[0], 'name': line[1],
                                    'address': line[2], 'phone_number': line[3],
                                    'email': line[4]}
                    mongo.customers.insert_one(new_customer)
                    customer_count += 1
        except (FileNotFoundError, KeyError, IndexError):
            customer_err += 1

        try:
            with open(os.path.join(directory_name, rentals_file)) as csv_file:
                rental_data = csv.reader(csv_file, delimiter=",")
                for line in rental_data:
                    new_rental = {'product_id': line[0], 'customer_id': line[1],
                                  'rental_start_date': line[2],
                                  'rental_end_date': line[3],
                                  'cost_per_day': line[4]}
                    mongo.rentals.insert_one(new_rental)
                    rental_count += 1
        except (FileNotFoundError, KeyError, IndexError):
            rental_err += 1

    return (product_count, customer_count, rental_count), (product_err,
                                                           customer_err,
                                                           rental_err)


def show_available_products():
    """
    :parm product_id:
    :return dict:
    """
    mongo = MongoDatabase()
    product_dict = dict()
    with mongo:
        available_products = mongo.products.find(
            {'quantity_available':{"$gt": "0"}})
        for product in available_products:
            product_dict[product['product_id']] = {
                'description':product['description'],
                'product_type':product['product_type'],
                'quantity_available':product['quantity_available']}
    return product_dict


def show_rentals(product_id):
    """return the dictionary object of customers who have rented in the past.
    :parm product_id:
    :parm dict:
    """
    mongo = MongoDatabase()
    rental_dict = dict()
    with mongo:
        renters = mongo.rentals.find({'product_id':product_id})
        for renter in renters:
            customer = mongo.customers.find_one({
                'customer_id':renter['customer_id']})
            rental_dict[renter['customer_id']] = {
                'name':customer['name'],
                'address':customer['address'],
                'phone_number':customer['phone_number'],
                'email':customer['email']}
    return rental_dict


if __name__ == "__main__":
    COUNT, ERROR = import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
    # print(show_available_products())
    for renter_id, renter_info in show_rentals('prd002').items():
        name = renter_info['name']
        print(name)
