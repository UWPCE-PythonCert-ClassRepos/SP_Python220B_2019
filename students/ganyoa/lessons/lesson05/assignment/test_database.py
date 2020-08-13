from database import *
import unittest


class TestDatabase(unittest.TestCase):


    def test_mongo_connection(self):
        LOGGER.info("test_mongo_connection section")
        mongo = MongoDBConnection()
        self.assertEqual(mongo.host, '127.0.0.1')
        self.assertEqual(mongo.port, 27017)


    def test_csv_import(self):
        LOGGER.info("test_csv_import section")
        drop_collection()
        import_data('data_files', 'products.csv', 'customers.csv', 'rentals.csv')

        mongo = MongoDBConnection()
        with mongo:

            norton_db = mongo.connection.hp_norton

            #confirm all collections were added to db
            self.assertEqual(sorted(norton_db.list_collection_names()),
                            ['customers', 'products', 'rentals'])

            #spot check one known data point
            cust_col = norton_db['customers']
            cust_info = {'customer_id': 'cust_003'}

            for x in cust_col.find(cust_info, { "_id": 0, 'name': 1}):
                self.assertEqual(x, {'name': 'Curt Cicada'})


    def test_import_data_return_value(self):
        LOGGER.info("test_import_data_return_value section")
        drop_collection()
        self.assertEqual(import_data('data_files', 'products.csv', 'customers.csv', 'rentalzz.csv'),
                        ((7, 5, 0), (0, 0, 1)))


    def test_available_products(self):
        LOGGER.info("test_available_products section")
        drop_collection()
        import_data('data_files', 'products.csv', 'customers.csv', 'rentals.csv')

        result = show_available_products()
        self.assertEqual(result['prd001']['quantity_available'], 5)
        self.assertEqual(result['prd004']['quantity_available'], 7)
        self.assertEqual(result['prd007']['quantity_available'], 4)


    def test_show_rentals(self):
        LOGGER.info("test_show_rentals section")
        drop_collection()
        import_data('data_files', 'products.csv', 'customers.csv', 'rentals.csv')

        self.assertEqual(show_rentals('prd005'),
            {'cust002': {'name': 'Bedelia Bollweevil',
             'address': '832 S. East Blvd',
             'phone number': '206-001-1234',
             'email': 'bb@email.com'},
             'cust004': {'name': 'Deepak Damselfly',
             'address': '6192 W. South St',
             'phone number': '360-001-1234',
             'email': 'dd@email.com'}})

