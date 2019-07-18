"""
Functions for using the MongoDB backend for our rentals app.
Uses autoload functionality of the ExpandedMongoDBConnection.
"""

import csv
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

DATABASE = None


def import_csv_to_mongodb(collection, csv_file_path):
    """Import a single CSV file into MongoDB."""
    with open(csv_file_path) as csv_file:
        result = collection.insert_many(csv.DictReader(csv_file))
        return len(result.inserted_ids)


def import_data(directory_name,
                product_file,
                customer_file,
                rentals_file,
                *,
                database=None):
    """
    Import data from multiple CSV files into MongoDB.
    """
    if not database:
        database = DATABASE
    customer = database['customer']
    product = database['product']
    rental = database['rental']

    counts = (
        import_csv_to_mongodb(product, f"{directory_name}/{product_file}"),
        import_csv_to_mongodb(customer, f"{directory_name}/{customer_file}"),
        import_csv_to_mongodb(rental, f"{directory_name}/{rentals_file}")
    )
    return counts


def show_available_products(*, database=None):
    """List all products that have quantity available != 0"""
    if not database:
        database = DATABASE
    products = database['product'].find({'quantity_available': {'$ne':'0'}})
    products_dict = {prod['product_id']:
                     {'description': prod['description'],
                      'product_type': prod['product_type'],
                      'quantity_available': int(prod['quantity_available'])}
                     for prod in products}
    return products_dict


def show_rentals(product_id, *, database=None):
    """List all customers that have rented a given product id."""
    if not database:
        database = DATABASE
    rentals = database['rental']\
        .find({'product_id': product_id})\
        .sort('customer_id')
    rental_list = [rental['customer_id'] for rental in rentals]
    customers = database['customer'].find({'customer_id':
                                           {'$in': rental_list}})
    cust_dict = {cust['customer_id']:
                 {'name': f'{cust["first_name"]} {cust["last_name"]}',
                  'address': cust["address"],
                  'phone_number': cust["phone"],
                  'email': cust["email"]}
                 for cust in customers}
    return cust_dict


def drop_data(database=None):
    """Drop all data from the currently selected database."""
    if not database:
        database = DATABASE
    database['product'].drop()
    database['customer'].drop()
    database['rental'].drop()


class ExpandedMongoDBConnection:
    """MongoDB Connection with some added useful features."""

    def __init__(self,
                 *,
                 host='127.0.0.1',
                 port=27017,
                 directory_name=None,
                 product_file=None,
                 customer_file=None,
                 rentals_file=None):
        """
        Can specify files to auto-load.
        Be sure to use the ip address not name for local windows
        """
        self.host = host
        self.port = port
        self.connection = None
        # Self import if everything is specified.
        self.import_counts = None
        if directory_name and product_file and customer_file and rentals_file:
            self.autoload_args = (directory_name, product_file, customer_file,
                                  rentals_file)

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        if self.autoload_args:
            self.import_counts = import_data(*self.autoload_args,
                                             database=self.connection.rentals)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


if __name__ == "__main__":
    MONGO = ExpandedMongoDBConnection(directory_name='data',
                                      product_file='products.csv',
                                      customer_file='customers.csv',
                                      rentals_file='rentals.csv')

    with MONGO:
        DATABASE = MONGO.connection.rentals

    logging.info('Imported %d products, %d customers, and %d rentals',
                 *MONGO.import_counts)

    PRODS = show_available_products()
    for prod in PRODS:
        print(prod, PRODS[prod])

    drop_data()
