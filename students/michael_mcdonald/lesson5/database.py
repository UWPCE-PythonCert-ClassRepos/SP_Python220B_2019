# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable=R0914
"""lesson 4 michael mcdonald """

import csv
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure

# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('database_lesson5.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """define host and port for the connection"""

        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        try:
            self.connection = MongoClient(self.host, self.port)
            logger.info('connection successful')
            return self
        except ConnectionFailure as e:
            logger.error('mongo connection error %s', e, exc_info=True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class ImportData:
    """a class to handle mongo data transactions"""

    mongo = MongoDBConnection()
    counter = 0

    def __init__(self, table_name='', file_location=''):
        self.table_name = table_name
        self.file_location = file_location

    def import_data(self):
        """Takes a directory name three csv files as input and returns 2 tuples:
        - a record count of the number of products, customers and rentals added (in that order),
        - a count of any errors"""

        with ImportData.mongo:
            # no connection, exit
            result_list = []
            if ImportData.mongo is None:
                return 'connection not found'
            try:
                tmp_csv_file = open(self.file_location, 'r')
                tmp_reader = csv.DictReader(tmp_csv_file)
            except FileNotFoundError:
                error_result = 'file import error: {} not found'.format(self.file_location)
                ImportData.counter += 1
                return error_result
            norton_db = ImportData.mongo.connection.NortonDB
            try:
                if self.table_name == 'customers':
                    header = ['user_id', 'name', 'address', 'phone_number',
                              'email']
                elif self.table_name == 'products':
                    header = ['product_id', 'description', 'product_type',
                              'quantity_available']
                elif self.table_name == 'rentals':
                    header = ['user_id', 'product_id']
                for each in tmp_reader:
                    row = {}
                    for field in header:
                        row[field] = each[field]
                    norton_db[self.table_name].insert_one(row)
            except OperationFailure as e:
                logger.error('mongo import error %s', e, exc_info=True)
                ImportData.counter += 1
            tmp_tables_list = ['customers', 'products', 'rentals']
            # the number of products, customers and rentals added
            for table in tmp_tables_list:
                tmp_str = table + ': ' + str(norton_db[table].count_documents({})) + ', '
                result_list.append(tmp_str)
            result_tuple = tuple(result_list)
            counter_list = [ImportData.counter]
            counter_tuple = tuple(counter_list)
            results = [result_tuple, counter_tuple]
            return results


class DropData:
    """drop tables class"""

    mongo = MongoDBConnection()

    def __init__(self, tables):
        self.tables = tables

    def drop_table(self):
        """drop all tables provided in the list"""

        # no connection, exit
        if DropData.mongo is None:
            return 'connection not found'
        with DropData.mongo:
            norton_db = DropData.mongo.connection.NortonDB
            try:
                for table in self.tables:
                    drop_table = norton_db[table]
                    drop_table.drop()
                result = 'all data dropped- good luck on your next job'
            except OperationFailure as e:
                logger.error('mongo drop table error %s', e, exc_info=True)
                result = 'mongo drop table error {}'.format(e)
        return result


class ShowProductsAndCustomers:
    """show products class"""

    mongo = MongoDBConnection()

    @staticmethod
    def see_products_for_rent():
        """return a list of all products"""

        if ShowProductsAndCustomers.mongo is None:
            return 'connection not found'
        with ShowProductsAndCustomers.mongo:
            norton_db = ShowProductsAndCustomers.mongo.connection.NortonDB
            products_list = []
            try:
                products = norton_db['products']
                products_collection = products.find()
                for document in products_collection:
                    products_list.append('{0}, qty available({1})'.
                                         format(document['description'],
                                                document['quantity_available']))
            except OperationFailure as e:
                logger.error('mongo retrieve table error %s', e, exc_info=True)
                products_list = ['mongo retrieve table error {}'.format(e)]
            if len(products_list) == 0:
                products_list.append('no products found')
        return products_list

    @staticmethod
    def see_all_different_products():
        """Returns a Python dictionary of products listed as available with the
        following fields: product_id, description, product_type, quantity_available"""

        if ShowProductsAndCustomers.mongo is None:
            return 'connection not found'
        with ShowProductsAndCustomers.mongo:
            norton_db = ShowProductsAndCustomers.mongo.connection.NortonDB
            products_list = []
            try:
                products = norton_db['products']
                products_collection = products.find()
                for document in products_collection:
                    products_list.append('{0}, {1}, {2}, '
                                         'qty avail({3})'.format(document['product_id'],
                                                                 document['description'],
                                                                 document['product_type'],
                                                                 document['quantity_available']))
            except OperationFailure as e:
                logger.error('mongo retrieve table error %s', e, exc_info=True)
                products_list = ['mongo retrieve table error {}'.format(e)]
            if len(products_list) == 0:
                products_list.append('no products found')
        return products_list

    @staticmethod
    def see_list_of_rental_details(product_id):
        """Returns a Python dictionary with the following user information
        from users that have rented products matching product_id:
        user_id, name, address, phone_number, email"""

        customer_rental_list = []
        if ShowProductsAndCustomers.mongo is None:
            return 'connection not found'
        with ShowProductsAndCustomers.mongo:
            norton_db = ShowProductsAndCustomers.mongo.connection.NortonDB
            try:
                rentals = norton_db['rentals']
                customers = norton_db['customers']
                user_id_list = []
                rentals_collection = rentals.find({'product_id': product_id})
                for product in rentals_collection:
                    user_id_list.append((product['user_id']))

                for user in user_id_list:
                    customer_collection = customers.find({'user_id': user})
                    for customer in customer_collection:
                        customer_rental_list.append('{0}, {1}, {2}, {3}, '
                                                    '{4}'.format(customer['user_id'],
                                                                 customer['name'],
                                                                 customer['address'],
                                                                 customer['phone_number'],
                                                                 customer['email']))
            except OperationFailure as e:
                logger.error('mongo retrieve data error %s', e, exc_info=True)
                customer_rental_list = ['mongo retrieve data error {}'.format(e)]
            if len(customer_rental_list) == 0:
                customer_rental_list.append('no rentals found')
        return customer_rental_list
