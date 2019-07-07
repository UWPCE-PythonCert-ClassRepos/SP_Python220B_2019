"""Functions for using the MongoDB backend for our rentals app."""

import csv
import logging
import time
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

DATABASE = None


class Stopwatch:  # pylint: disable=too-few-public-methods
    """Simple stopwatch for timing events."""
    def __init__(self):
        self.last = time.time_ns()
        self.start = self.last

    def mark(self):
        """Reset the clock time and return (total time, split time)."""
        now = time.time_ns()
        total_diff = (now - self.start) / 1_000_000_000
        split_diff = (now - self.last) / 1_000_000_000
        self.last = now
        return total_diff, split_diff

    def mark_and_log(self, message):
        """
        Same as mark but logs the supplied message along with total and split.
        """
        total, split = self.mark()
        logging.info("%s (split time: %f secs, total time: %f secs).",
                     message, split, total)


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


def import_product(csv_row):
    """Import product from csv row to MongoDB."""
    collection = DATABASE['product']
    collection.insert_one({'product_id':csv_row[0],
                           'description': csv_row[1],
                           'product_type': csv_row[2],
                           'quantity_available': csv_row[3]})


def import_customer(csv_row):
    """Import customer from csv row to MongoDB."""
    collection = DATABASE['customer']
    collection.insert_one({'first_name': csv_row[0],
                           'last_name': csv_row[1],
                           'address': csv_row[2],
                           'phone': csv_row[3],
                           'email': csv_row[4],
                           'customer_id': csv_row[5]})


def import_rental(csv_row):
    """Import rental from csv row to MongoDB."""
    collection = DATABASE['rental']
    collection.insert_one({'rental_id': csv_row[0],
                           'customer_id': csv_row[1],
                           'product_id': csv_row[2]})


def import_from_csv(csv_file_path, import_func):
    """Apply the import_func to every row in the csv."""
    with open(csv_file_path) as csv_file:
        csv_reader = csv.reader(csv_file)
        count = -1
        for row in csv_reader:
            count += 1
            if count == 0:  # skip the header row
                continue
            import_func(row)
        return count


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


# EXAMPLE RUN:
# INFO:root:Imported 10000 products.
# (split time: 3.413662 secs, total time: 3.413662 secs).
# INFO:root:Imported 10000 customers.
# (split time: 3.458679 secs, total time: 6.872341 secs).
# INFO:root:Imported 10000 rentals.
# (split time: 3.094805 secs, total time: 9.967146 secs).
if __name__ == "__main__":
    MONGO = MongoDBConnection()

    with MONGO:
        DATABASE = MONGO.connection.rentals

    STOPWATCH = Stopwatch()
    PROD_CT = import_from_csv('data/products.csv', import_product)
    STOPWATCH.mark_and_log(f"Imported {PROD_CT} products.")
    CUST_CT = import_from_csv('data/customers.csv', import_customer)
    STOPWATCH.mark_and_log(f"Imported {CUST_CT} customers.")
    RENT_CT = import_from_csv('data/rentals.csv', import_rental)
    STOPWATCH.mark_and_log(f"Imported {RENT_CT} rentals.")
    drop_data()
