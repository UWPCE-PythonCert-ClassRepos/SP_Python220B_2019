"""Basic Operation Unit Tests"""
import sys
sys.path.append('../')
from unittest import TestCase
import basic_operations
from customer_model import *

CUSTOMER_ID = 0
CUSTOMER_NAME = 1
CUSTOMER_LASTNAME = 2
CUSTOMER_HOME_ADDRESS = 3
CUSTOMER_PHONE_NUMBER = 4
CUSTOMER_EMAIL_ADDRESS = 5
CUSTOMER_STATUS = 6
CUSTOMER_CREDIT_LIMIT = 7

customers = [('1', 'Damien', 'Lillard', '456 Point Guard Ln', '503-555-1234', 'dlillard@trailblazers.com', True, 100000.00),
             ('2', 'CJ', 'McCollum', '308 Pinot Noir Rd', '503-555-9876', 'winesnob@trailblazers.com', True, 50000.00),
             ('3', 'Greg', 'Oden', '543 Bad Luck Heights', '808-555-9696', 'what@couldhavebeen.com', False, 100.00)]

class BasicOperationsIntegrationTest(TestCase):

    def tearDown(self):
        database.drop_tables([Customer])

    def test_basic_operations(self):
        for test_customer in customers:
            basic_operations.add_customer(test_customer[CUSTOMER_ID],
                                          test_customer[CUSTOMER_NAME],
                                          test_customer[CUSTOMER_LASTNAME],
                                          test_customer[CUSTOMER_HOME_ADDRESS],
                                          test_customer[CUSTOMER_PHONE_NUMBER],
                                          test_customer[CUSTOMER_EMAIL_ADDRESS],
                                          test_customer[CUSTOMER_STATUS],
                                          test_customer[CUSTOMER_CREDIT_LIMIT])

        customer = basic_operations.search_customer('1')
        self.assertEqual(customer.lastname, 'Lillard')

        basic_operations.update_customer_credit('2', 250.99)
        customer = basic_operations.search_customer('2')
        self.assertEqual(float(customer.credit_limit), 250.99)

        self.assertEqual(basic_operations.list_active_customers(), 2)

        self.assertEqual(basic_operations.delete_customer('3'), 1)

