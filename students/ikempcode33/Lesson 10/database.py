"""Database for contents of CSV files and integrates customer and product data"""
import os
import logging
import csv
from pymongo import MongoClient
import time

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


def timer_func(func):
    """function to time other functions"""
    def setup_logger(*args, **kwargs):
        log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
        log_file = 'timings.txt'

        formatter = logging.Formatter(log_format)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        start_time = time.time()
        out = func(*args, **kwargs)
        end_time = time.time()
        function_time = end_time - start_time
        logging.info('function: {}'.format(func.__name__))
        logging.info('time: {}'.format(function_time))
        if func.__name__ == 'import_data':
            num_records = sum(out[0])
            logging.info("processed records: {}".format(num_records))
        return out
    return setup_logger


# Read in CSV data
@timer_func
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
        customer.drop()
        product.drop()
        rental.drop()

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

@timer_func
def show_available_products():
    """Returns a dictionary of available products"""
    mongo = MongoDBConnection()
    with mongo:
        db = mongo.connection.media
        products = db['product']
        available_products = {}  #Dictionary output
        # Iterate through products for dict
        for item in products.find():
            available_products[item['product_id']] = {'description': item['description'],
                                                      'product_type': item['product_type'],
                                                      'quantity': item['quantity']}

        return available_products

@timer_func
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


if __name__ == '__main__':
    import_data('csv_data', 'products.csv', 'customers.csv', 'rentals.csv')
    import_data('csv_data', 'products_long.csv', 'customers_long.csv', 'rentals_long.csv')
    show_available_products()
    show_rentals('products')
