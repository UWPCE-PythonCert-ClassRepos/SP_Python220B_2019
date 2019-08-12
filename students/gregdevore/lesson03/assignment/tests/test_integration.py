'''
Integration tests for basic_operations module (Customer database API)
'''

import sys
# Add path to files
sys.path.append('/Users/gdevore21/Documents/Certificate Programs/Python/PYTHON220/ \
SP_Python220B_2019/students/gregdevore/lesson03/assignment')

from unittest import TestCase
from customer_model import database, Customer
import basic_operations

class ModuleTests(TestCase):
    '''
    Test suite for integration testing the basic_operations module

    Methods:
        test_module(self):
            Tests overall functionality, including adding customers to the
            database, deleting a customer from the database, and querying the
            current number of active customers in the database
    '''

    def test_module(self):
        '''
        Test overall basic_operations functionality
        '''

        # Set up empty table for testing
        database.drop_tables([Customer])
        database.create_tables([Customer])

        # Create new customers
        new_customer = {'id':'00001', 'firstname':'Ron', 'lastname':'Swanson',
                        'address':'123 Fake Street', 'phone':'555-867-5309',
                        'email':'ronswanson@pawnee.gov', 'status':0,
                        'credit_limit':10000}
        second_customer = {'id':'00002', 'firstname':'Leslie', 'lastname':'Knope',
                           'address':'345 Any Drive', 'phone':'555-867-5310',
                           'email':'leslieknope@pawnee.gov', 'status':1,
                           'credit_limit':20000}

        # Add customers
        for customer in [new_customer, second_customer]:
            basic_operations.add_customer(customer['id'],
                                          customer['firstname'],
                                          customer['lastname'],
                                          customer['address'], customer['phone'],
                                          customer['email'], customer['status'],
                                          customer['credit_limit'])

        # Delete a customer
        basic_operations.delete_customer(new_customer['id'])

        # Query number of active customers, should be 1
        num_active = basic_operations.list_active_customers()
        self.assertEqual(num_active, 1)
