# test_linear_parallel.py
""" This module defines all the test functions for linear.py  and
    parallel.py.
"""
import os
import cProfile
import pstats
from unittest import TestCase
import linear as db_linear
import parallel as db_para
import parallel_with_lock as db_para_lock
from generate_records import generate_data_file

class database_Tests(TestCase):
    """ This class defines unit test fuctions for database.py """
    def setUp(self):
        self.csv_file = 'csv_files_dr'
        self.product_file = 'products.csv'
        self.customer_file = 'customers.csv'
        self.rental_file = 'rentals.csv'

    def test_import_data(self):
        """ Test import_data() function """
        #db_linear.LOGGER.info('--- Start Test import_old_data() ---')
        db_linear.import_data(self.csv_file, self.product_file,
                              self.customer_file, self.rental_file)
        #db_linear.LOGGER.info('--- End Test import_old_data() ---')


class linear_Tests(TestCase):
    """ This class defines unit test fuctions for linear.py  and
        parallel.py
    """
    def setUp(self):
        self.record_num = 100006
        self.csv_file = 'csv_files_dr'
        self.product_file = 'products_thousand.csv'
        self.customer_file = 'customers_thousand.csv'
        self.rental_file = 'rentals_thousand.csv'

    def test_generate_data_file(self):
        """ Test generate_data_file() function """
        db_linear.LOGGER.info('\n\n--- Start Test generate_data_file() ---')
        # 1. generate the produrct .csv file.
        filename = os.path.join(self.csv_file, self.product_file)
        generate_data_file(self.record_num, filename, 1)
        self.assertEqual(os.path.exists(filename), True)

        # 2. generate the customer .csv file.
        filename = os.path.join(self.csv_file, self.customer_file)
        generate_data_file(self.record_num, filename, 2)
        self.assertEqual(os.path.exists(filename), True)

        #3.  generate the rental .csv file.
        filename = os.path.join(self.csv_file, self.rental_file)
        generate_data_file(self.record_num, filename, 3)
        self.assertEqual(os.path.exists(filename), True)
        db_linear.LOGGER.info('--- End Test generate_data_file() ---')

    def test_import_thousand_data(self):
        """ Test import_thousand_data() function """
        pr = cProfile.Profile()
        pr.enable()
        db_linear.LOGGER.info('\n\n--- Start Test import data linear ---')
        actual_res = db_linear.import_thousand_data(self.csv_file,
                                                    self.product_file,
                                                    self.customer_file,
                                                    self.rental_file)
        self.assertEqual(actual_res[0][0], 100000)
        self.assertEqual(actual_res[0][1], 5)
        self.assertEqual(actual_res[0][2], 100005)
        self.assertEqual(actual_res[1][0], 100000)
        self.assertEqual(actual_res[1][1], 5)
        self.assertEqual(actual_res[1][2], 100005)
        db_linear.LOGGER.info('--- End Test import data linear ---')
        # set up the profiling
        pr.disable()
        with open('linear.res', 'w') as file:
            ps = pstats.Stats(pr, stream=file)
            #ps.strip_dirs().sort_stats('time').print_stats()
            ps.strip_dirs().sort_stats('cumulative').print_stats(20)


class parallel_Tests(TestCase):
    """ This class defines unit test fuctions for parallel.py  and
        parallel_with_lock.py
    """
    def setUp(self):
        self.csv_file = 'csv_files_dr'
        self.product_file = 'products_throusand.csv'
        self.customer_file = 'customers_thousand.csv'
        self.rental_file = 'rentals_thousand.csv'

    def test_import_thousand_data_without_lock(self):
        """ Test import_thousand_data() function parallel """
        db_para.LOGGER.info('\n\n--- Start Test parallel without Lock ---')
        # generate the existing records.
        actual_res = db_linear.import_data(self.csv_file, 'products.csv',
                                           'customers.csv', 'rentals.csv')
        pr = cProfile.Profile()
        pr.enable()
        actual_res = db_para.import_thousand_data(self.csv_file,
                                                  self.product_file,
                                                  self.customer_file,
                                                  self.rental_file)
        self.assertEqual(actual_res[0][0], 100000)
        self.assertEqual(actual_res[0][1], 5)
        self.assertEqual(actual_res[0][2], 100005)
        self.assertEqual(actual_res[1][0], 100000)
        self.assertEqual(actual_res[1][1], 5)
        self.assertEqual(actual_res[1][2], 100005)
        db_para.LOGGER.info('--- End Test parallel without Lock ---')
        # set up the profiling
        pr.disable()
        with open('parallel_without_lock.res', 'w') as file:
            ps = pstats.Stats(pr, stream=file)
            #ps.strip_dirs().sort_stats('time').print_stats()
            ps.strip_dirs().sort_stats('cumulative').print_stats(20)

    def test_import_thousand_data_lock(self):
        """ Test import_thousand_data() function parallel with lock """
        db_para.LOGGER.info('\n\n--- Start Test parallel with lock ---')
        # generate the existing records.
        actual_res = db_linear.import_data(self.csv_file, 'products.csv',
                                           'customers.csv', 'rentals.csv')
        pr = cProfile.Profile()
        pr.enable()
        actual_res = db_para_lock.import_thousand_data(self.csv_file,
                                                       self.product_file,
                                                       self.customer_file,
                                                       self.rental_file)
        self.assertEqual(actual_res[0][0], 100000)
        self.assertEqual(actual_res[0][1], 5)
        self.assertEqual(actual_res[0][2], 100005)
        self.assertEqual(actual_res[1][0], 100000)
        self.assertEqual(actual_res[1][1], 5)
        self.assertEqual(actual_res[1][2], 100005)
        db_para.LOGGER.info('--- End Test parallel with lock ---')
        # set up the profiling
        pr.disable()
        with open('parallel_with_lock.res', 'w') as file:
            ps = pstats.Stats(pr, stream=file)
            ps.strip_dirs().sort_stats('cumulative').print_stats(20)
