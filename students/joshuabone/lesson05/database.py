"""Functions for using the MongoDB backend for our rentals app."""

import csv
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

DATABASE = None


class MongoDBConnection():
    """MongoDB Connection (copied from assignment example)"""

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


def import_csv_to_mongodb(collection, csv_file_path):
    """Import a single CSV file into MongoDB."""
    with open(csv_file_path) as csv_file:
        result = collection.insert_many(csv.DictReader(csv_file))
        return len(result.inserted_ids)


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    Import data from multiple CSV files into MongoDB.
    """
    customer = DATABASE['customer']
    product = DATABASE['product']
    rental = DATABASE['rental']

    counts = (
        import_csv_to_mongodb(product, f"{directory_name}/{product_file}"),
        import_csv_to_mongodb(customer, f"{directory_name}/{customer_file}"),
        import_csv_to_mongodb(rental, f"{directory_name}/{rentals_file}")
    )
    return counts


def show_available_products():
    """List all products that have quantity available != 0"""
    products = DATABASE['product'].find({'quantity_available': {'$ne':'0'}})
    products_dict = {prod['product_id']:
                     {'description': prod['description'],
                      'product_type': prod['product_type'],
                      'quantity_available': int(prod['quantity_available'])}
                     for prod in products}
    return products_dict


def show_rentals(product_id):
    """List all customers that have rented a given product id.s"""
    rentals = DATABASE['rental']\
        .find({'product_id': product_id})\
        .sort('customer_id')
    rental_list = [rental['customer_id'] for rental in rentals]
    customers = DATABASE['customer'].find({'customer_id':
                                           {'$in': rental_list}})
    cust_dict = {cust['customer_id']:
                 {'name': f'{cust["first_name"]} {cust["last_name"]}',
                  'address': cust["address"],
                  'phone_number': cust["phone"],
                  'email': cust["email"]}
                 for cust in customers}
    return cust_dict


def drop_data():
    """Drop all data from the currently selected database."""
    DATABASE['product'].drop()
    DATABASE['customer'].drop()
    DATABASE['rental'].drop()


if __name__ == "__main__":
    MONGO = MongoDBConnection()

    with MONGO:
        DATABASE = MONGO.connection.rentals

    CTS = import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
    logging.info('Imported %d products, %d customers, and %d rentals', *CTS)

    PRODS = show_available_products()
    for prod in PRODS:
        print(prod, PRODS[prod])

    drop_data()
