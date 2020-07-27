# Stella Kim
# Assignment 5: Consuming APIs with NoSQL

"""Migrate product data from a sample CSV file into MongoDB"""

import csv
import os
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """Initiate connection"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        """Establish connection to MongoDB"""
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits connection"""
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data file and return 2 tuples: the first with a record count of
    the number of products, customers and rentals added (in that order);
    the second with a count of any errors that occurred, in the same
    order.
    """
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.hp_norton
        product_count, product_errors = import_csv(directory_name,
                                                   product_file, database)
        customer_count, customer_errors = import_csv(directory_name,
                                                     customer_file, database)
        rentals_count, rentals_errors = import_csv(directory_name,
                                                   rentals_file, database)

    return ((product_count, customer_count, rentals_count),
            (product_errors, customer_errors, rentals_errors))


def import_csv(directory_name, collection_file, database):
    """Create collection in DB and import CSV file to insert into collection"""
    count = 0
    errors = 0
    try:
        filename = f'{collection_file}.csv'
        collection = database[collection_file]
        with open(os.path.join(directory_name, filename)) as file:
            collection.insert_many(data_convert(csv.DictReader(file)))
            count = collection.count_documents({})
    except OSError as err:
        print(f'OS error: {err}')
        errors = 1

    return count, errors


def data_convert(items):
    """Convert quantity available column in products file to integer form"""
    for item in items:
        converted_item = item.copy()
        if 'quantity_available' in item:  # convert columns
            converted_item['quantity_available'] =\
                int(item['quantity_available'])

        yield converted_item


def show_available_products():
    """Show all available products as a Python dictionary"""
    mongo = MongoDBConnection()
    available_products = {}
    with mongo:
        database = mongo.connection.hp_norton
        for product in database.products.find(
                        {'quantity_available': {'$gt': 0}}):
            available_products[product['product_id']] = {
                'description': product['description'],
                'product_type': product['product_type'],
                'quantity_available': product['quantity_available']}
    return available_products


def show_rentals(product_id):
    """Return user information for rented products matching product_id"""
    mongo = MongoDBConnection()
    rented_products = {}
    with mongo:
        database = mongo.connection.hp_norton
        for rental in database.rentals.find({'product_id': product_id}):
            for customer in database.customers.find({'user_id': rental['user_id']}):
                rented_products[customer['user_id']] = {
                    'name': customer['name'],
                    'address': customer['address'],
                    'phone_number': customer['phone_number'],
                    'email': customer['email']}
    return rented_products


def clear_collections():
    """Clear all collections from DB"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.hp_norton
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()


if __name__ == "__main__":
    clear_collections()
    import_data('./data/', 'products', 'customers', 'rentals')
    show_available_products()
    show_rentals('prd001')
