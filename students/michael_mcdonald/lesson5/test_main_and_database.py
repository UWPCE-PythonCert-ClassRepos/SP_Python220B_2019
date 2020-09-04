"""lesson 5 michael mcdonald """

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals

from unittest import TestCase
from unittest.mock import patch
import unittest.mock
import logging
import os
import csv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.errors import OperationFailure
import lesson5.database as mdb   # pylint: disable=import-error
import lesson5.main_lesson_5 as main   # pylint: disable=import-error

# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('test_database.log')
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

# cd C:\Users\mimcdona\Dropbox\UW\UW-Python220_Project\
# -m = load module
# python -m unittest lesson5\test_database.py
# python -m unittest lesson5\main_lesson5.py
# python -m coverage run --source=lesson5 -m unittest lesson5\test_database.py
# python -m coverage run --source=lesson5 -m unittest lesson5\main_lesson5.py
# python -m coverage report -m


class MongoDBConnectionTesting:
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


class ImportUnitTestData:
    """a class to handle mongo data transactions"""

    mongo = MongoDBConnectionTesting()
    counter = 0

    @staticmethod
    def import_data_handler():
        """import customer, product and rental csv files"""

        result = ''
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = ImportUnitTestData()
                result = mongo_insert.import_data(key, tmp_file)
                print(result)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
            print(result)
        return result

    # pylint: disable-msg=too-many-locals
    @staticmethod
    def import_data(table_name, file_location):
        """Takes a directory name three csv files as input and returns 2 tuples:
        - a record count of the number of products, customers and rentals added (in that order),
        - a count of any errors"""

        with ImportUnitTestData.mongo:
            # no connection, exit
            result_list = []
            if ImportUnitTestData.mongo is None:
                return 'connection not found'
            try:
                tmp_csv_file = open(file_location, 'r')
                tmp_reader = csv.DictReader(tmp_csv_file)
            except FileNotFoundError:
                error_result = 'file import error: {} not found'.format(file_location)
                ImportUnitTestData.counter += 1
                return error_result
            norton_db = ImportUnitTestData.mongo.connection.UnitTestNortonDB
            try:
                if table_name == 'customers':
                    header = ['user_id', 'name', 'address', 'phone_number',
                              'email']
                elif table_name == 'products':
                    header = ['product_id', 'description', 'product_type',
                              'quantity_available']
                elif table_name == 'rentals':
                    header = ['user_id', 'product_id']
                for each in tmp_reader:
                    row = {}
                    for field in header:
                        row[field] = each[field]
                    norton_db[table_name].insert_one(row)
            except OperationFailure as e:
                logger.error('mongo import error %s', e, exc_info=True)
                ImportUnitTestData.counter += 1
            tmp_tables_list = ['customers', 'products', 'rentals']
            # the number of products, customers and rentals added
            for table in tmp_tables_list:
                tmp_str = table + ': ' + str(norton_db[table].count_documents({})) + ', '
                result_list.append(tmp_str)
            result_tuple = tuple(result_list)
            counter_list = [ImportUnitTestData.counter]
            counter_tuple = tuple(counter_list)
            results = [result_tuple, counter_tuple]
        return results


class DropDataUnitTesting:
    """drop unittest data as needed """

    mongo = MongoDBConnectionTesting()

    @staticmethod
    def drop_data():
        """ drop tables before each test"""

        tables = ['customers', 'products', 'rentals']
        with DropDataUnitTesting.mongo:
            norton_db = DropDataUnitTesting.mongo.connection.UnitTestNortonDB
            try:
                for table in tables:
                    drop_table = norton_db[table]
                    drop_table.drop()
                result = 'table drop success'
            except OperationFailure as e:
                logger.error('mongo drop table error %s', e, exc_info=True)
                result = 'mongo drop table error {}'.format(e)
        print(result)


class TestMainLesson5(TestCase):
    """test main_lesson5"""

    m_in = ['1', '2', '3', '4', '5', '6', 'q']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def test_main_menu():
        """test main_menu"""

        with unittest.mock.patch('builtins.input',
                                 side_effect=TestMainLesson5.m_in) as main_menu_test:
            main.main_menu()
            main_menu_test.assert_has_calls([unittest.mock.call('>')])

    def test_drop_data_handler(self):
        """test drop data handler"""
        # insert some test data
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                print(mongo_insert)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
        result = main.drop_data_handler()
        self.assertEqual(result, 'all data dropped- good luck on your next job')

    def test_import_data_handler(self):
        """test import data handler"""

        # create new unittest data
        # unittest_result = ImportUnitTestData.import_data_handler()
        # test_result = main.import_data_handler()
        # print(test_result)
        # print(unittest_result)
        # self.assertEqual(test_result, unittest_result )


    def test_see_products_for_rent_handler(self):
        """test products for rent handler"""

        tables = ['customers', 'products', 'rentals']
        mongo_drop_table = mdb.DropData(tables)
        result = mongo_drop_table.drop_table()
        print(result)
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                result = mongo_insert.import_data()
                print(result)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
        my_products_list = main.see_products_for_rent_handler()
        self.assertEqual(len(my_products_list), 10)

    def test_see_all_different_products_handler(self):
        """test see all different products"""

        tables = ['customers', 'products', 'rentals']
        mongo_drop_table = mdb.DropData(tables)
        result = mongo_drop_table.drop_table()
        print(result)
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                result = mongo_insert.import_data()
                print(result)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
        my_products_list = main.see_all_different_products_handler()
        self.assertEqual(len(my_products_list), 10)

    @patch('builtins.input', side_effect=['f111e247-d90c-11ea-9997-287fcf638d95'])
    def test_see_list_of_rental_details_handler(self, mock_input):
        """test update credit"""

        result = main.see_list_of_rental_details_handler()
        self.assertEqual(result, 'c6d37ccb-d784-11ea-b075-287fcf638d95, Bob, '
                                 '122 Sycamore Lane, 122 123-4567, bob@email.com')
        print(mock_input)

    @classmethod
    def test_exit_program(cls):
        """text exit program"""

        with patch('sys.exit') as mock_exit_program:
            main.exit_program()
            assert mock_exit_program.called

class TestDatabase(TestCase):
    """test database classes and functions"""

    mongo = MongoDBConnectionTesting()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_import(self):
        """test data import class"""

        DropDataUnitTesting.drop_data()
        tup1 = ()
        tup2 = ()
        results = []
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                results = mongo_insert.import_data()
                tup1 = results[0]
                tup2 = results[1]
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
            print(result)
        print(results)
        print(tup1, tup2)
        # assert the correct number of items were added
        self.assertEqual(tup1[0], 'customers: 10, ')
        self.assertEqual(tup1[1], 'products: 10, ')
        self.assertEqual(tup1[2], 'rentals: 10, ')
        # check no errors occurred during addition
        self.assertEqual(tup2[0], 0)
        DropDataUnitTesting.drop_data()

    def test_drop(self):
        """test data drop class"""

        # create new data
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                results = mongo_insert.import_data()
                print(results)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
            print(result)
        with TestDatabase.mongo:
            norton_db = TestDatabase.mongo.connection.NortonDB
        tables = ['customers', 'products', 'rentals']
        mongo_drop_table = mdb.DropData(tables)
        result = mongo_drop_table.drop_table()
        print(result)
        for table in tables:
            document = norton_db[table]
            self.assertEqual(0, document.estimated_document_count())
            print(table, document.estimated_document_count())

    def test_see_all_different_products(self):
        """test see all different products"""

        # create new unittest data
        ImportUnitTestData.import_data_handler()
        # create new data
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                results = mongo_insert.import_data()
                print(results)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
            print(result)

        with TestDatabase.mongo:
            norton_db = TestDatabase.mongo.connection.NortonDB
            ut_prod = []
            try:
                products = norton_db['products']
                products_collection = products.find()
                for document in products_collection:
                    ut_prod.append('{0}, {1}, {2}, '
                                   'qty avail({3})'.format(document['product_id'],
                                                           document['description'],
                                                           document['product_type'],
                                                           document['quantity_available']))
            except OperationFailure as e:
                logger.error('mongo retrieve table error %s', e, exc_info=True)
                ut_prod = ['mongo retrieve table error {}'.format(e)]
            if len(ut_prod) == 0:
                ut_prod.append('no products found')
        test_prod_and_cust = mdb.ShowProductsAndCustomers()
        test_all_different_products = test_prod_and_cust.see_all_different_products()
        # two lists
        self.assertEqual(ut_prod, test_all_different_products)

    def test_see_list_of_rental_details(self):
        """test list_of_rental_details"""

        c_id = 'f111baf3-d90c-11ea-860f-287fcf638d95'
        # create new unittest data
        ImportUnitTestData.import_data_handler()
        # create new data
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                results = mongo_insert.import_data()
                print(results)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
            print(result)
        rental_products = mdb.ShowProductsAndCustomers()
        my_list = rental_products.see_list_of_rental_details(c_id)
        self.assertEqual(my_list[0],
                         'c6d37cca-d784-11ea-ba6e-287fcf638d95, '
                         'Alice, 121 Sycamore Lane, 121 123-4567, '
                         'alice@email.com')

    def test_see_products_for_rent(self):
        """test see products for rent"""

        # clean up
        DropDataUnitTesting.drop_data()
        tables = ['customers', 'products', 'rentals']
        mongo_drop_table = mdb.DropData(tables)
        result = mongo_drop_table.drop_table()
        print(result)
        # create new unittest data
        ImportUnitTestData.import_data_handler()
        with TestDatabase.mongo:
            norton_db = TestDatabase.mongo.connection.UnitTestNortonDB
            unittest_products_list = []
            try:
                products = norton_db['products']
                products_collection = products.find()
                for document in products_collection:
                    unittest_products_list.append('{0}, qty available({1})'.
                                                  format(document['description'],
                                                         document['quantity_available']))
            except OperationFailure as e:
                logger.error('mongo retrieve table error %s', e, exc_info=True)
                unittest_products_list = ['mongo retrieve table error {}'.format(e)]
            if len(unittest_products_list) == 0:
                unittest_products_list.append('no products found')
        # create new data
        try:
            current_dir = os.getcwd()
            directory_name = current_dir + '\\lesson5\\data\\'
            file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                              'rentals': 'rentals.csv'}
            for key, value in file_name_dict.items():
                tmp_file = directory_name + value
                mongo_insert = mdb.ImportData(key, tmp_file)
                results = mongo_insert.import_data()
                print(results)
        except FileNotFoundError as e:
            logger.error('exception %s', e, exc_info=True)
            result = 'exception {}'.format(e)
            print(result)
        test_products = mdb.ShowProductsAndCustomers()
        my_test_list = test_products.see_products_for_rent()
        self.assertEqual(my_test_list, unittest_products_list)
