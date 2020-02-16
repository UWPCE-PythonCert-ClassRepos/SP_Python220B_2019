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

    # add_customer(customers[0][CUST_ID], customers[0][NAME], customers[0][LAST_NAME],
#              customers[0][HOME_ADDRESS], customers[0][EMAIL_ADDRESS],
#              customers[0][PHONE], customers[0][STATUS], customers[0][CREDIT_LIMIT])

# add_customer(customers[1][CUST_ID], customers[1][NAME], customers[1][LAST_NAME],
#              customers[1][HOME_ADDRESS], customers[1][EMAIL_ADDRESS],
#              customers[1][PHONE], customers[1][STATUS], customers[1][CREDIT_LIMIT])

# add_customer(customers[2][CUST_ID], customers[2][NAME], customers[2][LAST_NAME],
#              customers[2][HOME_ADDRESS], customers[2][EMAIL_ADDRESS],
#              customers[2][PHONE], customers[2][STATUS], customers[2][CREDIT_LIMIT])

print(list_active_customers())