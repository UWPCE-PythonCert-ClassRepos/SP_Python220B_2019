'''
tests for the MongoDB database assignment
'''
from unittest import TestCase
from parallel import import_data, MongoDBConnection

def clear_db():
    mongo = MongoDBConnection()

    with mongo:
        db = mongo.connection.media
        product_db = db['product']
        customer_db = db['customer']
        rentals_db = db['rentals']
        product_db.drop()
        customer_db.drop()
        rentals_db.drop()

class MongoDBTest(TestCase):
    '''tests for basic operations'''

    def test_import_data(self):
        clear_db()
        '''tests csv files are imported correctly with
        correct tuples being returned'''
        test_import = import_data('csv_files', 'product_file.csv',
                                  'customer_file.csv', 'rental_file.csv')
        test_import_cust = test_import[0]
        test_import_prod = test_import[1]
        self.assertEqual(test_import_cust[0], 1000)
        self.assertEqual(test_import_cust[1], 0)
        self.assertEqual(test_import_cust[2], 1000)
        self.assertEqual(test_import_prod[0], 1000)
        self.assertEqual(test_import_prod[1], 0)
        self.assertEqual(test_import_prod[2], 1000)
