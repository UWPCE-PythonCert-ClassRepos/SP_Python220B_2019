"""
This module is to migrate the data from a sample csv file to Mongo DB
"""
import logging
import csv
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from types import FunctionType
import time

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class MongoDBConnection:
    def __init__(self, host='127.0.0.1', port=27017):
        """
        Initialize mongo connection
        :param host: Mongo host URL
        :param port: Mongo host port
        """
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        if self.connection is None:
            try:
                self.connection = MongoClient(self.host, self.port)
            except ConnectionFailure as e:
                LOGGER.error(f'Failed to connect to MongoDB. {e}')
                raise e
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes connection on exit
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.connection.close()


def time_log(func):
    def wrapper(self, *args, **kwargs):
        with open('timings.txt', 'a+', newline="") as output:
            start = time.time()
            old_count = {
                'products': self.database.products.count_documents({}),
                'customers': self.database.customers.count_documents({}),
                'rentals': self.database.rentals.count_documents({})
            }

            data = func(self, *args, **kwargs)

            new_count = {
                'products': self.database.products.count_documents({}),
                'customers': self.database.customers.count_documents({}),
                'rentals': self.database.rentals.count_documents({})
            }

            products = abs(old_count['products'] - new_count['products'])
            customers = abs(old_count['customers'] - new_count['customers'])
            rentals = abs(old_count['rentals'] - new_count['rentals'])
            time_duration = time.time() - start
            output.write(f'{func.__name__} processed '
                         f'{products} products, {customers} customers, '
                         f'{rentals} rentals. Took {time_duration} to run\n')

            return data
    return wrapper


class Timer(type):

    def __new__(cls, clsname, bases, clsdict):
        for attr, val in clsdict.items():
            if isinstance(val, FunctionType) and val.__name__ != '__init__':
                val = time_log(val)
            clsdict[attr] = val
        return super(Timer, cls).__new__(cls, clsname, bases, clsdict)


class HPNortonMongoDB(metaclass=Timer):
    """MongoDB Connection"""

    def __init__(self, connection):
        self.database = connection.connection.media

    def import_data(self, directory_name, product_file, customer_file,
                    rentals_file, flush = True):
        """
        Import data from csv file
        :param directory_name:
        :param product_file:
        :param customer_file:
        :param rentals_file:
        :return:
        """
        # Variables for counting the number of errors raised
        # when importing data.
        product_error_count = 0
        customer_error_count = 0
        rentals_error_count = 0
        product_file_path = os.path.join(directory_name, product_file)
        customer_file_path = os.path.join(directory_name, customer_file)
        rentals_file_path = os.path.join(directory_name, rentals_file)

        products = self.database["products"]
        customers = self.database["customers"]
        rentals = self.database["rentals"]

        if flush:
            # flush collections before insertion
            products.delete_many({})
            customers.delete_many({})
            rentals.delete_many({})

        try:
            with open(product_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    product_add = {
                        'product_id': str(row['product_id']),
                        'description': row['description'],
                        'product_type': row['product_type'],
                        'quantity_available': int(row['quantity_available'])
                    }

                    products.insert_one(product_add)

        except FileNotFoundError:
            product_error_count += 1

        try:
            with open(customer_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customer_add = {
                        'customer_id': row['customer_id'],
                        'name': row['name'],
                        'address': row['address'],
                        'phone_number': row['phone_number'],
                        'email': row['email']
                    }

                    customers.insert_one(customer_add)

        except FileNotFoundError:
            customer_error_count += 1

        try:
            with open(rentals_file_path, encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rentals_add = {
                        'customer_id': row['customer_id'],
                        'product_id': row['product_id'],
                        'quantity_available': int(row['quantity_available'])
                    }

                    rentals.insert_one(rentals_add)

        except FileNotFoundError:
            rentals_error_count += 1

        record_counts = (products.count_documents({}),
                         customers.count_documents({}),
                         rentals.count_documents({}))
        errors_count = (product_error_count, customer_error_count,
                        rentals_error_count)

        return record_counts, errors_count

    def show_available_product(self):
        """
        Show data of available product
        :return: the dict of available product information
        """
        products = self.database['products']
        result = dict()
        for prod in products.find({'quantity_available': {'$gt': 0}}):
            result[prod['product_id']] = {
                'product_id': prod['product_id'],
                'description': prod['description'],
                'product_type': prod['product_type'],
                'quantity_available': prod['quantity_available'],
            }

        return result

    def show_rentals(self, product_id):
        """
        Show information of rentals
        :param product_id: the id of products
        :return: dict of rentals infortmation
        """
        rentals = self.database['rentals']
        customers = self.database['customers']
        result = dict()

        for rental in rentals.find({'product_id': product_id}):
            customer_id = rental['customer_id']
            customer = customers.find_one({'customer_id': customer_id})
            result[customer_id] = {
                'user_id': rental['customer_id'],
                'name': customer['name'],
                'address': customer['address'],
                'phone_number': customer['phone_number'],
                'email': customer['email'],
            }

        return result


if __name__ == '__main__':
    with MongoDBConnection() as conn:
        MONGO = HPNortonMongoDB(conn)

        STATS = MONGO.import_data(directory_name='.',
                                  product_file='products.csv',
                                  customer_file='customers.csv',
                                  rentals_file='rental.csv',
                                  flush=False)

        AVAILABLE = MONGO.show_available_product()
        RENTALS = MONGO.show_rentals('prd001')

        print(STATS)
        print(AVAILABLE)
        print(RENTALS)
