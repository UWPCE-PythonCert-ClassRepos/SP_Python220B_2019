"""Unit testing"""

from unittest import TestCase
from peewee import DoesNotExist
from codes import basic_operations
from codes.customer_model import Customer, DATABASE
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('This is unit testing assignment for lesson03')

class CustomerTests(TestCase):
    """This is for unit testing basic_operation.py"""
    def setUp(self):
        '''this is for setting up a clean database'''
        DATABASE.drop_tables([Customer])
        DATABASE.create_tables([Customer])
        LOGGER.info('Database has been cleared and ready for new data')

    def add_customer_for_test(self):
        """Since we are resetting DB as part of set up, adding a function
        to quickly add a example data to db for testing purpose"""
        new_data = {'code':'A1', 'fname':'John', 'lname':'doe', 'address':'1004 ST SE', 
                    'phone':'206-555-1234', 'email':'johndoe@awesome.com', 'active':True,
                    'climit':7777}
        new_data2 = {'code':'A2', 'fname':'Sam', 'lname':'Wise', 'address':'315 Hampshire Dr.', 
                     'phone':'474-555-4477', 'email':'samwise@hobbits.com', 'active':False,
                     'climit':8888}
        for myinput in [new_data, new_data2]:
            basic_operations.add_customer(myinput['code'],
                                          myinput['fname'],
                                          myinput['lname'],
                                          myinput['address'],
                                          myinput['phone'],
                                          myinput['email'],
                                          myinput['active'],
                                          myinput['climit'])
        return new_data


    def test_add_customer_to_database(self):
        """This is for testing function in basic_operation.py for adding new
        customer"""

        LOGGER.info('New data will be entered into database')
        new_data = self.add_customer_for_test()
        customer = Customer.get(Customer.customer_id == new_data['code'])

        self.assertEqual(customer.customer_id, new_data['code'])
        self.assertEqual(customer.customer_name, new_data['fname'])
        self.assertEqual(customer.lastname, new_data['lname'])
        self.assertEqual(customer.home_address, new_data['address'])
        self.assertEqual(customer.phone_number, new_data['phone'])
        self.assertEqual(customer.email_address, new_data['email'])
        self.assertEqual(customer.customer_status, new_data['active'])
        self.assertEqual(customer.credit_limit, new_data['climit'])

        new_data = {'code':'A1', 'fname':'John', 'lname':'doe', 'address':'1004 ST SE', 
                    'phone':'206-555-1234', 'email':'johndoe@awesome.com', 'active':True,
                    'climit':7777}

        basic_operations.add_customer(new_data['code'],
                                      new_data['fname'],
                                      new_data['lname'],
                                      new_data['address'],
                                      new_data['phone'],
                                      new_data['email'],
                                      new_data['active'],
                                      new_data['climit'])

    def test_search_customer(self):
        """This is for testing seach function"""

        LOGGER.info('Data will be searched in this test')
        new_data = self.add_customer_for_test()
        myresult1 = basic_operations.search_customer('A3')
        myresult2 = basic_operations.search_customer('A1')

        LOGGER.info('See if empty dict is returned if searched nonexisting ID')
        self.assertEqual(myresult1, {})

        LOGGER.info('See if search is done correctly for existing ID')
        LOGGER.info(f'What is in myresult2?: {myresult2}')

        self.assertEqual(myresult2['firstname'], new_data['fname'])
        self.assertEqual(myresult2['lastname'], new_data['lname'])
        self.assertEqual(myresult2['email'], new_data['email'])
        self.assertEqual(myresult2['phone'], new_data['phone'])

    def test_delete_customer(self):
        """This is for testing delete function"""

        LOGGER.info('Data will be added and deleted')
        self.add_customer_for_test()
        LOGGER.info('Check if the data is added to db')
        myresult = Customer.get(Customer.customer_id == 'A1')
        LOGGER.info(f'What is in myresult?: {myresult}')

        LOGGER.info('Check if the data is deleted in the db')
        basic_operations.delete_customer('A1')
        with self.assertRaises(DoesNotExist):
            Customer.get(Customer.customer_id == 'A1')

        basic_operations.delete_customer('A3')

    def test_update_credit(self):
        """This is for testing update credit function"""

        LOGGER.info('Customer credit limit will be updated')
        self.add_customer_for_test()

        myresult = basic_operations.update_customer_credit('A3', 8888)
        LOGGER.info(f'Customer credit limit should be updated to {myresult}')
        self.assertEqual(myresult, ValueError)

        myresult = basic_operations.update_customer_credit('A1', 8888)
        LOGGER.info(f'Customer credit limit should be updated to {myresult}')
        self.assertEqual(myresult, 8888)

    def test_listing_active_customer(self):
        """This is for testing listing function for active customer"""

        LOGGER.info('Testing listing function')

        self.add_customer_for_test()

        myresult = basic_operations.list_active_customers()
        self.assertEqual(myresult, 1)






