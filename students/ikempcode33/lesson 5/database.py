"""Database for contents of CSV files and integrates customer and product data"""
import os
import csv
from pymongo import MongoClient


class MongoDBConnection():
    """MongoDBConnection"""

    def __init__(self, host='127.0.0.1', port=27017):
        self.host = host
        self.port = port
        self.connection = None


    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


# Read in CSV data
def import_data(directory_name, product_file, customer_file, rentals_file):
    """Takes in csv files, counts customers, products and rentals and errors"""
    # set to zero
    customer_errors = 0
    product_errors = 0
    rental_errors = 0
    customer_count = 0
    product_count = 0
    rental_count = 0
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        customer = db["customer"]
        product = db["product"]
        rental = db["rental"]
        customer.drop
        product.drop
        rental.drop

        try:
            with open(os.path.join(directory_name, customer_file)) as csv_file:
                cust_reader = csv.reader(csv_file, delimiter=',')
                firstline = True
                for row in cust_reader:
                    if firstline:
                        firstline = False
                        continue
                    customer_count += 1
                    customer_info = {'customer_id': row[0], 'name': row[1], 'address': row[2],
                                     'phone': row[3], 'email': row[4]}
                    customer.insert_one(customer_info)
        except FileNotFoundError:
            customer_errors += 1
        try:
            with open(os.path.join(directory_name, product_file)) as csv_file:
                prod_read = csv.reader(csv_file, delimiter=',')
                firstline = True
                for row in prod_read:
                    if firstline:
                        firstline = False
                        continue
                    product_count += 1
                    product_info = {'product_id': row[0], 'description': row[1], 'product_type': row[2],
                                    'quantity': row[3]}
                    product.insert_one(product_info)
        except FileNotFoundError:
            product_errors += 1
        try: 
            with open(os.path.join(directory_name, rentals_file)) as csv_file:
                rent_read = csv.reader(csv_file, delimiter=',')
                firstline = True
                for row in rent_read:
                    if firstline:
                        firstline = False
                        continue
                    rental_count += 1
                    info = {'customer_id': row[0], 'product_id': row[1]}
                    rental.insert_one(info)
        except FileNotFoundError:
            rental_errors += 1
    return ((customer_count, product_count, rental_count),
            (customer_errors, product_errors, rental_errors))


def show_available_products():
    """Returns a dictionary of available products"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        products = db['products']
        available_products = {}  #Dictionary output
        # Iterate through products for dict
        for item in products.find():
            available_products[item['product_id']] = {'description': item['description'],
                                                      'product_type': item['product_type'],
                                                      'quantity': item['quantity']}

        return available_products


def show_rentals(product_id):
    """Returns info of customers that have rented a product using the database"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        rentals = db['rental']
        rental_data = {}
        for row in rentals.find({'product_id': product_id}):
            result = db.customer.find_one({'customer_id': row['customer_id']})
            rental_data[result['customer_id']] = {'name': result['name'], 'address': result['address'],
                                                  'phone': result['phone'],
                                                  'email': result['email']}
    return rental_data
