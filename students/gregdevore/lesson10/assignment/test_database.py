'''
Insert docstring
'''
import os
from unittest import TestCase
from database import import_data, import_csv_to_json, add_json_to_mongodb
from database import show_available_products, show_rentals, MongoDBConnection
from database import create_mongo_connection

class DBTests(TestCase):
    '''
    Test suite for unit testing the database module
    Methods:
        setUpClass(cls):
            Class method, run before any tests, clears Customer database,
            creates new customer
        tearDown():
            Class method, drops databases after each test is run
        load_data():
            Static method called by multiple tests, adds CSV data to mongo
            database
        test_csv_to_json(self):
            Test method to convert CSV files to JSON format
        test_bad_csv_to_json(self):
            Test method to confirm behavior when bad CSV file is passed
        test_json_to_mongo(self):
            Test method to add JSON data to mongo database
        test_import_data(self):
            Test method to read CSV data, convert to JSON, and add to mongo
            database
        test_available_products(self):
            Test method to find all available products
        test_show_rentals(self):
            Test method to show customers who are renting a particular product
        test_show_rentals_empty(self):
            Test method to confirm behavior when product with no rentals is
            queried
        test_bad_connection(self):
            Test method to ensure bad mongo DB connection is properly handled
        test_bad_show_available(self):
            Test method to ensure bad mongo DB connection is properly handled
        test_bad_show_rentals(self):
            Test method to ensure bad mongo DB connection is properly handled
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Defines expected JSON data for CSV files
        '''
        cls.product_json = [{'product_id': 'prd001', 'description': 'sofa',
                             'product_type': 'livingroom', 'quantity_available': '4'},
                            {'product_id': 'prd002', 'description': 'coffee table',
                             'product_type': 'livingroom', 'quantity_available': '2'},
                            {'product_id': 'prd003', 'description': 'lounge chair',
                             'product_type': 'livingroom', 'quantity_available': '0'},
                            {'product_id': 'prd004', 'description': 'refrigerator',
                             'product_type': 'kitchen', 'quantity_available': '2'},
                            {'product_id': 'prd005', 'description': 'microwave',
                             'product_type': 'kitchen', 'quantity_available': '5'},
                            {'product_id': 'prd006', 'description': 'toaster',
                             'product_type': 'kitchen', 'quantity_available': '1'},
                            {'product_id': 'prd007', 'description': 'night stand',
                             'product_type': 'bedroom', 'quantity_available': '6'},
                            {'product_id': 'prd008', 'description': 'dresser',
                             'product_type': 'bedroom', 'quantity_available': '0'},
                            {'product_id': 'prd009', 'description': 'queen mattress',
                             'product_type': 'bedroom', 'quantity_available': '3'},
                            {'product_id': 'prd010', 'description': 'queen box spring',
                             'product_type': 'bedroom', 'quantity_available': '3'}]

        cls.customer_json = [{'user_id': 'user001', 'name': 'Jake Peralta',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0001',
                              'email': 'jperalta@brooklyn.pd'},
                             {'user_id': 'user002', 'name': 'Rose Diaz',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0002',
                              'email': 'rdiaz@brooklyn.pd'},
                             {'user_id': 'user003', 'name': 'Terry Jeffords',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0003',
                              'email': 'tjeffords@brooklyn.pd'},
                             {'user_id': 'user004', 'name': 'Amy Santiago',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0004',
                              'email': 'asantiago@brooklyn.pd'},
                             {'user_id': 'user005', 'name': 'Charles Boyle',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0005',
                              'email': 'cboyle@brooklyn.pd'},
                             {'user_id': 'user006', 'name': 'Ray Holt',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0006',
                              'email': 'rholt@brooklyn.pd'},
                             {'user_id': 'user007', 'name': 'Gina Linetti',
                              'address': '123 Precinct Lane', 'phone_number': '917-555-0007',
                              'email': 'glinetti@brooklyn.pd'}]

        cls.rentals_json = [{'rental_id': 'rnt001', 'customer_id': 'user003',
                             'product_id': 'prd001'},
                            {'rental_id': 'rnt002', 'customer_id': 'user005',
                             'product_id': 'prd005'},
                            {'rental_id': 'rnt003', 'customer_id': 'user002',
                             'product_id': 'prd004'},
                            {'rental_id': 'rnt004', 'customer_id': 'user006',
                             'product_id': 'prd009'},
                            {'rental_id': 'rnt005', 'customer_id': 'user006',
                             'product_id': 'prd010'},
                            {'rental_id': 'rnt006', 'customer_id': 'user001',
                             'product_id': 'prd002'},
                            {'rental_id': 'rnt007', 'customer_id': 'user002',
                             'product_id': 'prd001'},
                            {'rental_id': 'rnt008', 'customer_id': 'user002',
                             'product_id': 'prd005'}]

    @classmethod
    def tearDown(cls):
        '''
        Drop mongo collections after each test to ensure a fresh start
        '''
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.HPNorton
            db['product'].drop()
            db['customer'].drop()
            db['rentals'].drop()

    @staticmethod
    def load_data():
        '''
        Static method to load CSV data, convert to JSON, and add to mongo
        database
        '''
        import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')

    def test_csv_to_json(self):
        '''
        Test method to convert CSV files to JSON format
        '''
        directory = 'data'
        product_file = 'products.csv'
        customer_file = 'customers.csv'
        rentals_file = 'rentals.csv'

        product_json_actual, _ = import_csv_to_json(
            os.path.join(directory, product_file))
        customer_json_actual, _ = import_csv_to_json(
            os.path.join(directory, customer_file))
        rentals_json_actual, _ = import_csv_to_json(
            os.path.join(directory, rentals_file))

        self.assertEqual(self.product_json, product_json_actual)
        self.assertEqual(self.customer_json, customer_json_actual)
        self.assertEqual(self.rentals_json, rentals_json_actual)

    def test_bad_csv_to_json(self):
        '''
        Test method to confirm behavior when bad CSV file is passed
        '''
        return_data, error_count = import_csv_to_json('fake_file')
        self.assertEqual(return_data, [])
        self.assertEqual(error_count, 1)

    def test_json_to_mongo(self):
        '''
        Test method to add JSON data to mongo database
        '''
        product_counts = add_json_to_mongodb(self.product_json, 'product')
        customer_counts = add_json_to_mongodb(self.customer_json, 'customer')
        rentals_counts = add_json_to_mongodb(self.rentals_json, 'rentals')
        self.assertEqual(product_counts, (10, 0))
        self.assertEqual(customer_counts, (7, 0))
        self.assertEqual(rentals_counts, (8, 0))

    def test_import_data(self):
        '''
        Test method to read CSV data, convert to JSON, and add to mongo
        database
        '''
        counts, errors = import_data('data', 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(counts, (10, 7, 8))
        self.assertEqual(errors, (0, 0, 0))

    def test_available_products(self):
        '''
        Test method to find all available products
        '''
        available_expected = {'prd001': {'description': 'sofa',
                                         'product_type': 'livingroom',
                                         'quantity_available': '4'},
                              'prd002': {'description': 'coffee table',
                                         'product_type': 'livingroom',
                                         'quantity_available': '2'},
                              'prd004': {'description': 'refrigerator',
                                         'product_type': 'kitchen',
                                         'quantity_available': '2'},
                              'prd005': {'description': 'microwave',
                                         'product_type': 'kitchen',
                                         'quantity_available': '5'},
                              'prd006': {'description': 'toaster',
                                         'product_type': 'kitchen',
                                         'quantity_available': '1'},
                              'prd007': {'description': 'night stand',
                                         'product_type': 'bedroom',
                                         'quantity_available': '6'},
                              'prd009': {'description': 'queen mattress',
                                         'product_type': 'bedroom',
                                         'quantity_available': '3'},
                              'prd010': {'description': 'queen box spring',
                                         'product_type': 'bedroom',
                                         'quantity_available': '3'}}

        self.load_data()
        product_dict = show_available_products()

        self.assertEqual(product_dict, available_expected)

    def test_show_rentals(self):
        '''
        Test method to show customers who are renting a particular product
        '''
        rentals_expected = {'user002': {'name': 'Rose Diaz',
                                        'address': '123 Precinct Lane',
                                        'phone_number': '917-555-0002',
                                        'email': 'rdiaz@brooklyn.pd'},
                            'user003': {'name': 'Terry Jeffords',
                                        'address': '123 Precinct Lane',
                                        'phone_number': '917-555-0003',
                                        'email': 'tjeffords@brooklyn.pd'}}

        self.load_data()
        rentals_dict = show_rentals('prd001')

        self.assertEqual(rentals_dict, rentals_expected)

    def test_show_rentals_empty(self):
        '''
        Test method to confirm behavior when product with no rentals is
        queried
        '''
        self.load_data()
        self.assertEqual({}, show_rentals('prd999'))

    def test_bad_connection(self):
        '''
        Test method to ensure bad mongo DB connection is properly handled
        '''
        mongo = create_mongo_connection(host='127.0.0.1', port=27018)
        item_counts = add_json_to_mongodb([{'test':'test'}], 'zzz', mongo)
        self.assertEqual(item_counts, (0, 1))

    def test_bad_show_available(self):
        '''
        Test method to ensure bad mongo DB connection is properly handled
        '''
        mongo = create_mongo_connection(host='127.0.0.1', port=27018)
        product_dict = show_available_products(mongo)
        self.assertEqual(product_dict, {})

    def test_bad_show_rentals(self):
        '''
        Test method to ensure bad mongo DB connection is properly handled
        '''
        mongo = create_mongo_connection(host='127.0.0.1', port=27018)
        rentals_dict = show_rentals('prd001', mongo)
        self.assertEqual(rentals_dict, {})
