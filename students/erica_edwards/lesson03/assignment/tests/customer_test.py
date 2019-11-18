"""
Test basic_operations
"""

# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=too-many-arguments
# pylint: disable=invalid-name

import logging
from unittest import TestCase
import peewee
from customer_model import *
from basic_operations import *


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Started logger')

database = SqliteDatabase('customer.db')
database.connect()


class BasicOperationsTests(TestCase):
    """Testing basic_operations.py"""

    def setUp(self):
        """setting up database with customer"""
        database.create_tables([Customer])

    def tearDown(self):
        """Clear database tables"""
        database.drop_tables([Customer])

    def test_add_customer(self):
        """Test customer added"""

        customer = {'customer_id':            'D421',
                    'customer_name':          'Susie',
                    'customer_last_name':     'Smith',
                    'customer_address':       '2424 No Name Rd',
                    'customer_phone_number':  '4256789255',
                    'customer_email':         'susies@yahoo.com',
                    'customer_status':        True,
                    'customer_credit_limit':  9000.00
                    }
        result = add_customer(**customer)
        self.assertEqual(result.customer_id, customer['customer_id'])

    def test_add_customer_again_fail(self):
        """Check if error is raised"""

        customer = {'customer_id':            'D421',
                    'customer_name':          'Susie',
                    'customer_last_name':     'Smith',
                    'customer_address':       '2424 No Name Rd',
                    'customer_phone_number':  '4256789255',
                    'customer_email':         'susies@yahoo.com',
                    'customer_status':        True,
                    'customer_credit_limit':  9000.00
                    }
        result = add_customer(**customer)
        self.assertEqual(result.customer_id, customer['customer_id'])
        with self.assertRaises(peewee.IntegrityError):
            result = add_customer(**customer)



    def test_search_customer(self):
        """Test if search return correct customer"""

        customer = {'customer_id':            'D422',
                    'customer_name':          'Kelly',
                    'customer_last_name':     'Smith',
                    'customer_address':       '2423 No Name Rd',
                    'customer_phone_number':  '4256799255',
                    'customer_email':         'kelly@yahoo.com',
                    'customer_status':        True,
                    'customer_credit_limit':  9000.00
                    }
        add_customer(**customer)
        expected = {'customer_name': customer['customer_name'],
                    'customer_last_name': customer['customer_last_name'],
                    'customer_email': customer['customer_email'],
                    'customer_phone_number': customer['customer_phone_number']}

        actual = search_customer(customer['customer_id'])

        self.assertEqual(expected, actual)

        LOGGER.info('Test exception is triggered')
        result = search_customer('F926')
        self.assertNotEqual(actual, result)

    def test_delete_customer(self):
        """Test is customer is deleted"""
        customer = {'customer_id':            'D422',
                    'customer_name':          'Kelly',
                    'customer_last_name':     'Smith',
                    'customer_address':       '2423 No Name Rd',
                    'customer_phone_number':  '4256799255',
                    'customer_email':         'kelly@yahoo.com',
                    'customer_status':        True,
                    'customer_credit_limit':  9000.00
                    }
        add_customer(**customer)

        result = delete_customer(customer['customer_id'])
        self.assertTrue(result == 1)

    def test_update_customer_credit(self):
        """Test customer credit limit is updated"""
        customer = {'customer_id':            'D422',
                    'customer_name':          'Kelly',
                    'customer_last_name':     'Smith',
                    'customer_address':       '2423 No Name Rd',
                    'customer_phone_number':  '4256799255',
                    'customer_email':         'kelly@yahoo.com',
                    'customer_status':        True,
                    'customer_credit_limit':  9000.00
                    }
        current_limit = customer['customer_credit_limit']
        add_customer(**customer)
        update_customer_credit(customer['customer_id'], 8000.00)
        new_limit = Customer.get(Customer.customer_id == customer['customer_id']).customer_credit_limit
        self.assertNotEqual(current_limit, new_limit)


    def test_update_customer_credit_exception(self):
        """Test value error is raised"""

        with self.assertRaises(ValueError):
            LOGGER.info('Starting update customer credit')
            update_customer_credit("D428", 8500.00)


    def test_list_active_customers(self):
        """Test active customers queury"""
        customer = {'customer_id':            'D422',
                    'customer_name':          'Kelly',
                    'customer_last_name':     'Smith',
                    'customer_address':       '2423 No Name Rd',
                    'customer_phone_number':  '4256799255',
                    'customer_email':         'kelly@yahoo.com',
                    'customer_status':         True,
                    'customer_credit_limit':   9000.00
                   }
        add_customer(**customer)

        result = list_active_customers()
        self.assertTrue(result == 1)
