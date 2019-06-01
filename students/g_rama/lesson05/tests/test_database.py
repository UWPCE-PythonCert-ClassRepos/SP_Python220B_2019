"""Testing the database.py"""
import logging
import unittest
import sys
sys.path.append('/Users/guntur/PycharmProjects/uw/p220/SP_Python220B_2019/'
                'students/g_rama/lesson05/src/')
import database


class TestDatabase(unittest.TestCase):

    def test_import_data(self, directory_name, product_file, customer_file, rentals_file):
        """Testing """
        database.import_data(directory_name, product_file, customer_file, rentals_file)

    def test_show_available_products(self):
        pass

    def test_show_rentals(self):
        pass
