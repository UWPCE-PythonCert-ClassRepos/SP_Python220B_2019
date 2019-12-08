'''
Tests basic operations and customer model integrated
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
from basic_operations import display_customers
from customer_model import Customer, DB

class TestIntegration(TestCase):
    '''
    This class tests the integrated test
    '''
    def setUp(self):
        DB.create_tables([Customer])

    def tearDown(self):
        Customer.delete().execute()
        DB.close()

    def test_integration(self):
        '''
        This fucntion tests the model and basic_fuctions classes
        '''
        add_customer(300, 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        add_customer(400, 'Jane', 'Doe', '200 Main St', '123-456-6789',
                     'janedoe@gmail.com', 'inactive', 20000)
        displayed_customers = ['Customer: 300' + '\n'
                               'Name: John' + '\n'
                               'Last Name: Doe' + '\n'
                               'Home Address: 100 Main St' + '\n'
                               'Phone Number: 123-456-6789' + '\n'
                               'Email Address: johndoe@gmail.com' + '\n'
                               'Status: active' + '\n'
                               'Credit Limit: 10000' + '\n' + '\n',
                               'Customer: 400' + '\n'
                               'Name: Jane' + '\n'
                               'Last Name: Doe' + '\n'
                               'Home Address: 200 Main St' + '\n'
                               'Phone Number: 123-456-6789' + '\n'
                               'Email Address: janedoe@gmail.com' + '\n'
                               'Status: inactive' + '\n'
                               'Credit Limit: 20000' + '\n' + '\n']

        self.assertEqual(display_customers(), displayed_customers)
        searched_dict = search_customer(300)
        self.assertEqual(search_customer(500), {})
        self.assertEqual(searched_dict, {'name': 'John', 'lastname': 'Doe',
                                         'email_address': 'johndoe@gmail.com',
                                         'phone_number': '123-456-6789'})
        self.assertEqual(list_active_customers(), 1)
        update_customer_credit(300, 40000)
        updated_customer = Customer.select().where(Customer.customer_id == 300).get()
        self.assertEqual(updated_customer.credit_limit, 40000)
        with self.assertRaises(ValueError):
            update_customer_credit(500, 20000)
        delete_customer(300)
        number = delete_customer(400)
        self.assertEqual(number, 1)
        number = delete_customer(500)
        self.assertEqual(number, 0)
        self.assertEqual(list_active_customers(), 0)
        add_customer('abc', 'John', 'Doe', '100 Main St', '123-456-6789',
                     'johndoe@gmail.com', 'active', 10000)
        customer = Customer.get_or_none()
        self.assertIsNone(customer)
