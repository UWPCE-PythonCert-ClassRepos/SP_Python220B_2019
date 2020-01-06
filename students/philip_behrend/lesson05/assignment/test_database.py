import pandas as pd
from unittest import TestCase
from database import *
from pymongo import MongoClient



class DatabaseTests(TestCase):
    """ Tests for database.py file """

    def setUp(self):
        mongo = MongoDBConnection()
        with mongo:
            db = mongo.connection.NortonFurniture

            products = db["products"]
            customers = db["customers"]
            rentals = db["rentals"]

        # Start with empty collections
            products.drop()
            customers.drop()
            rentals.drop()

            import_file('products.csv', 'customers.csv', 'rentals.csv')
        return db 

    def test_mongodbconnection(self):
        t1 = MongoDBConnection()
        self.assertEqual(t1.host, '127.0.0.1')
        self.assertEqual(t1.port, 27017)
        #how would we test the mongo client here?


    def test_import_file(self):
        db = self.setUp()

        # Create test dicts from input data
        product_data = pd.read_csv('products.csv')
        customer_data = pd.read_csv('customers.csv')
        rental_data = pd.read_csv('rentals.csv')

        product_data = product_data.to_dict('records')
        customer_data = customer_data.to_dict('records')
        rental_data = rental_data.to_dict('records')


        for i, item in db['products'].find()[0].items():
            if i != '_id':
                self.assertEqual(item, product_data[0][i])

        for i, item in db['customers'].find()[0].items():
            if i != '_id':
                self.assertEqual(item, customer_data[0][i])

        for i, item in db['rentals'].find()[0].items():
            if i != '_id':
                self.assertEqual(item, rental_data[0][i])

    def test_import_file_return(self):
        db = self.setUp()
        result = import_file('products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(result, ((4, 5, 5), (0, 0, 0)))

    def test_show_available_products(self):
        db = self.setUp()
        result = show_available_products()
        expected = {'prd001': {'description': '60-in tv',
                    'product_type': 'livingroom',
                    'quantity_available': 3},
                    'prd002': {'description': 'L-shaped sofa',
                    'product_type': 'livingroom',
                    'quantity_available': 1},
                    'prd003': {'description': 'wood table',
                    'product_type': 'kitchen',
                    'quantity_available': 5},
                    'prd004': {'description': 'ping-pong table',
                    'product_type': 'rec_room',
                    'quantity_available': 1}}
        self.assertEqual(result,expected)

    def test_show_rentals(self):
        db = self.setUp()

        result = show_rentals('prd004')

        expected = {'user0001': {'name': 'John Deere',
                    'address': '999 Main Street',
                    'phone': '206-993-9999'},
                    'user0002': {'name': 'Jackie Smith',
                    'address': '104 1st Street',
                    'phone': '206-206-2060'}}
        self.assertEqual(result,expected)