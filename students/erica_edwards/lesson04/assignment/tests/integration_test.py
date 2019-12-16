"""
Test integration
"""
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unnecessary-pass
# pylint: disable=unused-import

import logging
import unittest
# from unittest import TestCase
import peewee
from customer_model import *
from basic_operations import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Started logger')

# Setup tables for testing
database.drop_tables([Customer])
database.create_tables([Customer])


class BasicOperationsIntegrationTests(unittest.TestCase):
    """Testing basic_operations functionality"""

    def setUp(self):
        "Checking if tables created"
        print('\nIn setUp()')
        tables = database.get_tables()
        print(tables)
        if "Customer" not in tables:
            database.create_tables([Customer])

    def test_integration(self):
        """
        Test add, delete, and active functions.
        """
        # Build customer data

        customer1 = {'customer_id':           'D421',
                     'customer_name':          'Susie',
                     'customer_last_name':     'Smith',
                     'customer_address':       '2424 No Name Rd',
                     'customer_phone_number':  '4256789255',
                     'customer_email':         'susies@yahoo.com',
                     'customer_status':        True,
                     'customer_credit_limit':  9000.00
                     }

        customer2 = {'customer_id':           'D845',
                     'customer_name':          'Willie',
                     'customer_last_name':     'Snow',
                     'customer_address':       '246 No Name Rd',
                     'customer_phone_number':  '4256789256',
                     'customer_email':         'willie@yahoo.com',
                     'customer_status':        False,
                     'customer_credit_limit':  9000.00
                     }

        customer3 = {'customer_id':           'D451',
                     'customer_name':          'Bea',
                     'customer_last_name':     'Home',
                     'customer_address':       '2424 Home Rd',
                     'customer_phone_number':  '4256789288',
                     'customer_email':         'beahome@yahoo.com',
                     'customer_status':        True,
                     'customer_credit_limit':  9000.00
                     }

        # Add customer data
        for customer in [customer1, customer2, customer3]:
            try:
                add_customer(**customer)
            except peewee.IntegrityError as ex:
                LOGGER.info("Record already exists: continuing")
                LOGGER.info(ex)
        LOGGER.info('Data added')

        # Search for customer to confirm added
        customer_number = 'D421'
        search_dict = {'customer_name': 'Susie',
                       'customer_last_name': 'Smith',
                       'customer_email': 'susies@yahoo.com',
                       'customer_phone_number': '4256789255'}

        result = search_customer(customer_number)
        self.assertEqual(search_dict, result)

        # delete customer
        delete_customer('D421')

        # Check for one active customer
        active_customers = list_active_customers()
        self.assertEqual(active_customers, 1)

    def test_nothing(self):
        """workaround to fix hanging VSCode test runner"""
        pass
