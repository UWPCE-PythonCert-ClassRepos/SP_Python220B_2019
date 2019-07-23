"""
Victor
"""

from unittest import TestCase
from database import import_data, show_available_products
from database import show_rentals
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


class TestDatabase(TestCase):
    """"test for database.py"""

    def test_import_data(self):
        test_import = import_data('data', 'inventory.csv', 'customers.csv',
                                  'rentals.csv')
        self.assertEqual(test_import, ((0, 0, 0), (1, 1, 1)))

    def test_show_rentals(self):
        self.assertEqual(show_rentals('1234'), {})

    def test_show_available_products(self):
        self.assertEqual(show_available_products(), {})
