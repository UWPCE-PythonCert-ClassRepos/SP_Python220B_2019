"""Module to test database module"""
import sys
import csv
from unittest import TestCase
sys.path.append('database')
import database

mydir = "/Users/calvin/Documents/python_work/SP_Online_PY220/SP_Python220B_2019/students/calvinf/lesson_05/assignment_05"


class ModuleTests(TestCase):
    """Class to test integration of inventory management """
    maxDiff = None

    def setUp(self):
        """
        write initial test data to csv
        """

        product_file = [
            ('product_id', 'description', 'product_type', 'quantity'),
            ('prd001', '60 - inch TV stand', 'livingroom', 0),
            ('prd002', 'Black 240 watt Oven', 'Kitchen', 1),
            ('prd003', 'Brown faux fur love seat', 'livingroom', 0),
            ('prd004', 'U - shaped Love seat', 'livingroom', 0),
            ('prd005', 'L - shaped patio sofa', 'Outdoor', 0),
            ('prd006', 'White two drawer freezer', 'Kitchen', 3)]

        customer_file = [
            ('user_id', 'first_name', 'last_name', 'address', 'phone_number', 'email'),
            ('user001', 'Calvin', 'Fannin', '3145 Woodlane', '206-345-7895', 'calvin.fannin@birds.com'),
            ('user002', 'Elisa', 'Miles', '7853 Elliot Ave', '253-345-0986', 'elisa.miles@yahoo.com'),
            ('user003', 'Maya', 'Datumn', '4566 Cherry Street', '425-345-2413', 'mdata@uw.edu'),
            ('user004', 'Devon', 'Dude', '689 Park Ave', '845-345-3674', 'devonthedude@gmail.com'),
            ('user005', 'Ztephen', 'Zleming', '498789 Moolokiaiin', '206-345-4332', 'flemingsp@hotmail.com')
            ,('user006', 'Stephen', 'Fleming', '498789 Moolokiaiin', '206-345-4332', 'flemings@hotmail.com')
            ]

        # Rental
        rental_file = [
            ('rental_id', 'user_id', 'product_id'),
            ('rnt001', 'user001', 'prd001'),
            ('rnt001', 'user001', 'prd002'),
            ('rnt003', 'user005', 'prd002'),
            ('rnt004', 'user004', 'prd002'),
            ('rnt005', 'user002', 'prd004')]

        files = {"product.csv": product_file, "customer.csv": customer_file, "rental.csv": rental_file}
        for k, v in files.items():
            with open(k, 'w') as data_file:
                data_file_writer = csv.writer(data_file)
                data_file_writer.writerows(v)

        database.import_data(mydir, 'product.csv', 'customer.csv', 'rental.csv')

    def test_import_data_fail(self):
        """Run import with same csv files to generate errors """
        expected = (0, 0, 5), (6, 6, 0)
        result = database.import_data(mydir, 'product.csv', 'customer.csv', 'rental.csv')
        self.assertEqual(result, expected)

    def test_select_avail_products(self):
        """Test that available products are returned correctly"""
        expected = [{'product_id': 'prd002', 'description': 'Black 240 watt Oven', 'product_type': 'Kitchen', 'quantity': 1},
                    {'product_id': 'prd006', 'description': 'White two drawer freezer', 'product_type': 'Kitchen', 'quantity': 3}]
        result = database.show_available_products()
        self.assertEqual(result, expected)

    def test_search_rentals(self):
        """Testing the Rental search returns correctly"""
        expected = [{'product_id': 'prd001', 'user_id': 'user001', 'name': 'Calvin Fannin', 'address': '3145 Woodlane',
          'phone_number': '206-345-7895', 'email': 'calvin.fannin@birds.com'}]
        result = database.show_rentals('prd001')
        self.assertEqual(result, expected)

    def test_search_rentals_not_found(self):
        """Testing the Rental search returns nothing when given id that doesnt exist"""
        expected = []
        result = database.show_rentals('prd0017')
        self.assertEqual(result, expected)

    def tearDown(self):
        """Delete database after test cases have ran"""
        # pass
        database.CLIENT.drop_database('storedata')
