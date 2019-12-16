"""tests for basic operations """
# pylint: disable=unnecessary-comprehension
from unittest import TestCase
import csv
import os
from database import import_csv, import_data, drop_collections, MongoDBConnection
from database import show_rentals, show_available_products, insert_into_table

# Current directory
PATH = os.getcwd() + '\\'


def database_setup():
    """function for setting up clean table each time"""
    mongo = MongoDBConnection()
    with mongo:
        database = mongo.connection.myDB

    for collection in database.list_collection_names():
        database[collection].drop()

    return database


def build_test_csvs():
    """Build the test CSVs to test on"""
    with open('customers.csv', 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',')
        file_writer.writerow(['user_id', 'name', 'address', 'phone', 'email'])
        file_writer.writerow(['user001', 'Guy Dudeman', '1139 Bro Street',
                              '800-123-4567', 'Guy_Dudeman01@gmail.com'])

    with open('products.csv', 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',')
        file_writer.writerow(['product_id', 'description', 'product_type', 'quantity_available'])
        file_writer.writerow(['prd001', '60-inch TV stand', 'livingroom', 3])

    with open('rentals.csv', 'w') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',')
        file_writer.writerow(['rental_id', 'product_id', 'customer_id',
                              'amount', 'time', 'price', 'total'])
        file_writer.writerow(['rnt001', 'prd001', 'user001', 1, 7, 10, 70])


def delete_test_csv():
    """Removes the test csvs"""
    os.remove('customers.csv')
    os.remove('products.csv')
    os.remove("rentals.csv")


class TestBasicOps(TestCase):
    """Class for housing the tests"""

    def test_import_csv(self):
        """imports a csv from a file path and makes a json"""
        build_test_csvs()

        test = import_csv('customers.csv')
        self.assertEqual(test['data'][0]['user_id'], 'user001')
        self.assertEqual(test['data'][0]['name'], 'Guy Dudeman')
        self.assertEqual(test['data'][0]['address'], '1139 Bro Street')
        self.assertEqual(test['data'][0]['phone'], '800-123-4567')
        self.assertEqual(test['data'][0]['email'], 'Guy_Dudeman01@gmail.com')
        self.assertEqual(test['data'][0]['user_id'], 'user001')
        self.assertEqual(test['errors'], 0)

        test = import_csv('products.csv')
        self.assertEqual(test['data'][0]['product_id'], 'prd001')
        self.assertEqual(test['data'][0]['description'], '60-inch TV stand')
        self.assertEqual(test['data'][0]['product_type'], 'livingroom')
        self.assertEqual(test['data'][0]['quantity_available'], '3')
        self.assertEqual(test['errors'], 0)

        test = import_csv('rentals.csv')
        self.assertEqual(test['data'][0]['rental_id'], 'rnt001')
        self.assertEqual(test['data'][0]['product_id'], 'prd001')
        self.assertEqual(test['data'][0]['customer_id'], 'user001')
        self.assertEqual(test['data'][0]['amount'], '1')
        self.assertEqual(test['data'][0]['time'], '7')
        self.assertEqual(test['data'][0]['price'], '10')
        self.assertEqual(test['data'][0]['total'], '70')
        self.assertEqual(test['errors'], 0)

        delete_test_csv()

    def test_insert_into_table(self):
        """takes json and sticks into database"""
        database = database_setup()
        test_dicts = [{'person': 'Maveric'},
                      {'person': 'Charlie'},
                      {'person': 'Iceman'},
                      {'person': 'Goose'},
                      {'person': 'Viper'},
                      {'person': 'Jester'},
                      {'person': 'Couger'},
                      {'person': 'Wolfman'},
                      {'person': 'Slider'}]

        insert_into_table('test', test_dicts)

        for test_value in test_dicts:
            query = database.test.find(filter={"person": test_value['person']},
                                       projection={'_id': False})
            self.assertEqual([values["person"] for values in query][0], test_value['person'])

        database.test.drop()


    def test_import_data(self):
        """Test the import of data"""
        build_test_csvs()
        database = database_setup()
        test = import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')
        self.assertEqual(test, ((1, 1, 1), (0, 0, 0)))
        database.test.drop()
        delete_test_csv()

    def test_drop_collections(self):
        """test building a table, check if it exists,
         then drop it and make sure it reuturns nothing"""
        database = database_setup()
        test_dicts = [{'person': 'Maveric'},
                      {'person': 'Charlie'},
                      {'person': 'Iceman'},
                      {'person': 'Goose'},
                      {'person': 'Viper'},
                      {'person': 'Jester'},
                      {'person': 'Couger'},
                      {'person': 'Wolfman'},
                      {'person': 'Slider'}]

        insert_into_table('test', test_dicts)
        for test_value in test_dicts:
            query = database.test.find(filter={"person": test_value['person']},
                                       projection={'_id': False})
            self.assertEqual([values["person"] for values in query][0], test_value['person'])

        drop_collections()
        query = database.test.find()

        self.assertEqual([values for values in query], [])

    def test_show_rentals(self):
        '''show user info that have rented'''
        build_test_csvs()
        database = database_setup()
        import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')

        customers = import_csv(PATH + 'customers.csv')['data']
        rentals = import_csv(PATH + 'rentals.csv')['data']
        for rental in rentals:
            query_results = show_rentals(rental['product_id'])
            csv_results = \
                [next(cust for cust in customers if cust["user_id"] == rental['customer_id'])]
            self.assertEqual(query_results,
                             {customer.pop('user_id'): customer for customer in csv_results})
        database.test.drop()
        delete_test_csv()

    def test_show_available_products(self):
        '''show user info that have rented'''
        build_test_csvs()
        database = database_setup()
        import_data(PATH, 'products.csv', 'customers.csv', 'rentals.csv')

        products = import_csv(PATH + 'products.csv')['data']
        for row in products:
            row['quantity_available'] = int(row['quantity_available'])
        csv_results = [next(prod for prod in products if int(prod['quantity_available']) > 0)]
        self.assertEqual(show_available_products(),
                         {product.pop('product_id'): product for product in csv_results})

        database.test.drop()
        delete_test_csv()
