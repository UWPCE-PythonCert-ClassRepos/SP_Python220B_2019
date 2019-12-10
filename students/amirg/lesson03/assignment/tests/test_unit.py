'''
Tests each function in basic operations and customer model
'''
#pylint: disable=import-error
#pylint: disable=wrong-import-position
import sys
sys.path.append('../src')
from unittest import TestCase
from basic_operations import add_customer
from basic_operations import search_customer
from basic_operations import delete_customer
from basic_operations import update_customer_credit
from basic_operations import list_active_customers
from customer_model import Customer, DB


class CustomerModelTests(TestCase):
    '''
    Sets up tests for customer model module
    '''
    def setUp(self):
        DB.create_tables([Customer])

    def tearDown(self):
        Customer.delete().execute()
        DB.close()


class BasicOperationsTests(TestCase):
    '''
    Sets up tests for basic operations module
    '''
    def setUp(self):
        DB.create_tables([Customer])

    def tearDown(self):
        Customer.delete().execute()
        DB.close()

    def test_add_customer(self):
        '''
        Tests if customer is added, returns none if not able to add
        '''
        add_customer(300, 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)

        self.assertEqual(Customer[300].customer_id, 300)
        self.assertEqual(Customer[300].name, 'John')
        self.assertEqual(Customer[300].lastname, 'Doe')
        self.assertEqual(Customer[300].home_address, '100 Main St')
        self.assertEqual(Customer[300].phone_number, '123-456-6789')
        self.assertEqual(Customer[300].email_address, 'johndoe@gmail.com')
        self.assertEqual(Customer[300].status, 'active')
        self.assertEqual(Customer[300].credit_limit, 10000)

        delete_customer(300)
        #add logic here for not being able to add
        add_customer('abc', 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        customer = Customer.get_or_none()
        self.assertIsNone(customer)

    def test_search_customer(self):
        '''
        Tests if customer search is successfull, or returns blank
        dict if not successful
        '''
        add_customer(300, 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        searched_dict = search_customer(300)
        equalled_dict = {'name': 'John', 'lastname': 'Doe',
                         'email_address': 'johndoe@gmail.com',
                         'phone_number': '123-456-6789'}
        self.assertEqual(searched_dict, equalled_dict)
        empty_dict = {}
        searched_dict = search_customer(400)
        self.assertEqual(searched_dict, empty_dict)

    def test_delete_customer(self):
        '''
        Tests if customer gets deleted or will return 0 if not
        '''
        add_customer(300, 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        number = delete_customer(300)
        number2 = delete_customer(400)
        #add logic here to check whether its empty
        self.assertEqual(number, 1)
        #add logic here for attempting to delete non-existing ID
        self.assertEqual(number2, 0)

    def test_update_customer_credit(self):
        '''
        Tests if customer credit gets updated, returns value error if not
        '''
        add_customer(300, 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        update_customer_credit(300, 20000)
        updated_customer = Customer.select().where(Customer.customer_id == 300).get()
        self.assertEqual(updated_customer.credit_limit, 20000)
        with self.assertRaises(ValueError):
            update_customer_credit(400, 20000)

    def test_list_active_customers(self):
        '''
        Tests if correct number of active customers is listed
        '''
        add_customer(300, 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        add_customer(400, 'Jane', 'Doe', '200 Main St', '123-456-6789',
                     'janedoe@gmail.com', 'inactive', 20000)
        self.assertEqual(list_active_customers(), 1)
