"""
This module is to migrate the data from a sample csv file to Mongo DB
"""
import logging
import csv
import time
from collections import defaultdict
from pathlib import Path
from pymongo import MongoClient
from threading import Lock, Thread

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


class HPNortonMongoDB:
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """
        Initialize mongo connection
        :param host: Mongo host URL
        :param port: Mongo host port
        """
        self.host = host
        self.port = port
        self.connection = MongoClient(self.host, self.port)
        self.database = self.connection.media

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes connection on exit
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.connection.close()

    @staticmethod
    def import_data(filename: Path, collection, count_dict):
        now = time.time()
        try:
            LOCK.acquire()
            with filename.open(encoding='utf-8-sig') as file:
                base_name = filename.name
                reader = csv.DictReader(file)

                if base_name == PRODUCTS_PATH:
                    count_dict['products_before_count'] = \
                        collection.count_documents({})
                    for row in reader:
                        product_add = {
                            'product_id': str(row['product_id']),
                            'description': row['description'],
                            'product_type': row['product_type'],
                            'quantity_available': int(row['quantity_available'])
                        }
                        collection.insert_one(product_add)
                        count_dict['products_inserted'] += 1

                    count_dict['products_after_count'] =\
                        count_dict['products_before_count'] +\
                        count_dict['products_inserted']
                    count_dict['products_time'] = time.time() - now

                elif base_name == CUSTOMERS_PATH:
                    count_dict['customers_before_count'] = \
                        collection.count_documents({})
                    for row in reader:
                        customer_add = {
                            'customer_id': row['customer_id'],
                            'name': row['name'],
                            'address': row['address'],
                            'phone_number': row['phone_number'],
                            'email': row['email']
                        }
                        collection.insert_one(customer_add)
                        count_dict['customers_inserted'] += 1

                    count_dict['customers_after_count'] =\
                        count_dict['customers_before_count'] +\
                        count_dict['customers_inserted']
                    count_dict['customers_time'] = time.time() - now

                elif base_name == RENTAL_PATH:
                    for row in reader:
                        rentals_add = {
                            'customer_id': row['customer_id'],
                            'product_id': row['product_id'],
                            'quantity_available': int(row['quantity_available'])
                        }
                        collection.insert_one(rentals_add)
                else:
                    count_dict['error'] += 1

            LOCK.release()

        except FileNotFoundError:
            LOCK.release()

    def import_data_parent(self, directory_name, product_file, customer_file,
                           rentals_file, flush=False):
        """
        Import data from csv file
        :param directory_name:
        :param product_file:
        :param customer_file:
        :param rentals_file:
        :param flush:
        :return:
        """
        counts = defaultdict(lambda: 0)

        product_file_path = Path(directory_name / product_file)
        customer_file_path = Path(directory_name / customer_file)
        rentals_file_path = Path(directory_name / rentals_file)

        products = self.database["products"]
        customers = self.database["customers"]
        rentals = self.database["rentals"]

        if flush:
            # flush collections before insertion
            products.delete_many({})
            customers.delete_many({})
            rentals.delete_many({})

        product_thread = Thread(target=self.import_data,
                                args=(product_file_path, products,
                                      counts))
        product_thread.start()

        customer_thread = Thread(target=self.import_data,
                                 args=(customer_file_path, customers,
                                       counts))
        customer_thread.start()

        rental_thread = Thread(target=self.import_data,
                               args=(rentals_file_path, rentals,
                                     counts))
        rental_thread.start()

        product_thread.join()
        customer_thread.join()
        rental_thread.join()

        products_result = (
            counts['products_inserted'], counts['products_before_count'],
            counts['products_after_count'], counts['products_time']
        )
        customers_result = (
            counts['customers_inserted'], counts['customers_before_count'],
            counts['customers_after_count'], counts['customers_time']
        )

        return [products_result, customers_result]

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
    LOCK = Lock()
    MONGO = HPNortonMongoDB()
    PRODUCTS_PATH = 'products.csv'
    CUSTOMERS_PATH = 'customers.csv'
    RENTAL_PATH = 'rental.csv'
    STATS = MONGO.import_data_parent(Path('.'),
                                     PRODUCTS_PATH,
                                     CUSTOMERS_PATH,
                                     RENTAL_PATH, flush=True)

    AVAILABLE = MONGO.show_available_product()
    RENTALS = MONGO.show_rentals('prd001')

    print(STATS)
    print(AVAILABLE)
    print(RENTALS)
