# test_database.py
""" This module defines all the test functions for database.py """
import random
from unittest import TestCase
import database as db


class database_Tests(TestCase):
    """ This class defines unit test fuctions for database.py """
    def setUp(self):
        self.csv_file = 'csv_files_dr'

    # the input file has 5 records
    def test_import_1(self):
        """ Test import_1() function """
        product_file = 'products_5.csv'
        customer_file = 'customers_5.csv'
        rental_file = 'rentals_5.csv'
        db.LOGGER.info('--- Start Test import_data() ---')
        db.import_data(self.csv_file, product_file,
                       customer_file, rental_file)

        the_dict = db.show_available_products()
        db.LOGGER.info(f'Tot {len(the_dict)} products are available for rent.')

        prd_num = 'prd00' + str(random.randint(1, 5))
        the_dict = db.show_rentals(prd_num)
        db.LOGGER.info(f'The customers info for renting product: {prd_num}')
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test import_data() ---')

    # the input file has hundred records
    def test_import_2(self):
        """ Test import_1() function """
        product_file = 'products_hundred.csv'
        customer_file = 'customers_hundred.csv'
        rental_file = 'rentals_hundred.csv'
        db.LOGGER.info('--- Start Test import_data() ---')
        db.import_data(self.csv_file, product_file,
                       customer_file, rental_file)

        the_dict = db.show_available_products()
        db.LOGGER.info(f'Tot {len(the_dict)} products are available for rent.')

        prd_num = 'prd' + str(random.randint(6, 105))
        the_dict = db.show_rentals(prd_num)
        db.LOGGER.info(f'The customers info for renting product: {prd_num}')
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test import_data() ---')

    # the input file has thousand records
    def test_import_3(self):
        """ Test import_1() function """
        product_file = 'products_thousand.csv'
        customer_file = 'customers_thousand.csv'
        rental_file = 'rentals_thousand.csv'
        db.LOGGER.info('--- Start Test import_data() ---')
        db.import_data(self.csv_file, product_file,
                       customer_file, rental_file)

        the_dict = db.show_available_products()
        db.LOGGER.info(f'Tot {len(the_dict)} products are available for rent.')

        prd_num = 'prd' + str(random.randint(6, 1005))
        the_dict = db.show_rentals(prd_num)
        db.LOGGER.info(f'The customers info for renting product: {prd_num}')
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test import_data() ---')

    # the input file has ten thousand records
    def test_import_4(self):
        """ Test import_1() function """
        product_file = 'products_ten_thousand.csv'
        customer_file = 'customers_ten_thousand.csv'
        rental_file = 'rentals_ten_thousand.csv'
        db.LOGGER.info('--- Start Test import_data() ---')
        db.import_data(self.csv_file, product_file,
                       customer_file, rental_file)

        the_dict = db.show_available_products()
        db.LOGGER.info(f'Tot {len(the_dict)} products are available for rent.')

        prd_num = 'prd' + str(random.randint(6, 10005))
        the_dict = db.show_rentals(prd_num)
        db.LOGGER.info(f'The customers info for renting product: {prd_num}')
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test import_data() ---')

    # the input file has hundred thousand records
    def test_import_5(self):
        """ Test import_1() function """
        product_file = 'products_hundred_thousand.csv'
        customer_file = 'customers_hundred_thousand.csv'
        rental_file = 'rentals_hundred_thousand.csv'
        db.LOGGER.info('--- Start Test import_data() ---')
        db.import_data(self.csv_file, product_file,
                       customer_file, rental_file)

        the_dict = db.show_available_products()
        db.LOGGER.info(f'Tot {len(the_dict)} products are available for rent.')

        prd_num = 'prd' + str(random.randint(6, 100005))
        the_dict = db.show_rentals(prd_num)
        db.LOGGER.info(f'The customers info for renting product: {prd_num}')
        for key, val in the_dict.items():
            db.LOGGER.info(f"-- \'{key}\': {val}")
        db.LOGGER.info('--- End Test import_data() ---')
