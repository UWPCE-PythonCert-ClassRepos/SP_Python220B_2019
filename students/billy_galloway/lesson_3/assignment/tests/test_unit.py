'''
Unit testing module
'''
from unittest import TestCase
from unittest.mock import patch
import peewee
from basic_operations import *



class DatabaseTests(TestCase):
    ''' Database test class '''
    def setUp(self):
        ''' 
        setup database and handle connections and closure 
        '''
        pass


    def test_database_created(self):
        ''' test database connection '''
        pass

    def test_customer_model(self):
        ''' 
        Tests to ensure all the elements of the customer model
        are present

        Customer model elemenets:
            customer id
            name
            lastname
            home address
            email address
            status
            credit limit
        '''
        pass

    def test_basic_operations(self):
        ''' 
        Tests that basic operations are functioning
        basic operations:
            add_customer
            search_customer
            delete_customer
            update_customer
            list_active_customer
        '''
        pass

    