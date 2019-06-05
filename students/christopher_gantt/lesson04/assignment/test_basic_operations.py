'''Testing for basic_operations.py'''
import logging
from unittest import TestCase
from peewee import *
from hp_norton_model import *
from basic_operations import add_customer, search_customer, delete_customer
from basic_operations import update_customer_credit, list_active_customers

#pylint Disable=wildcard-import, unused-wildcard-import

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')

database.init('test.db')
LOGGER.info('test.db created for tests')

class BasicOperationsTests(TestCase):
    '''testing basic_operation.py'''
    def setUp(self):
        '''sets up the database for unit testing'''
        database.drop_tables([Customer])
        database.create_tables([Customer])

        LOGGER.info('creating a customer for test, John Coder')
        customer = ('D123', 'John', 'Coder', '12345 High St W', 4258291234,
                    'johncoder@gmail.com', True, 10500)
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer[0],
                first_name=customer[1],
                last_name=customer[2],
                home_address=customer[3],
                phone_number=customer[4],
                email_address=customer[5],
                activity_status=customer[6],
                credit_limit=customer[7])
            new_customer.save()
        LOGGER.info('setup for test complete')

    def test_add_customer(self):
        '''tests add_customer function'''
        add_customer('C123', 'Cody', 'Coder', '12345 High St W', 4258291234,
                     'codycoder@gmail.com', True, 10500)
        customer = Customer.get(Customer.customer_id == 'C123')
        self.assertEqual(customer.customer_id, 'C123')
        self.assertEqual(customer.first_name, 'Cody')
        self.assertEqual(customer.last_name, 'Coder')
        self.assertEqual(customer.home_address, '12345 High St W')
        self.assertEqual(customer.phone_number, 4258291234)
        self.assertEqual(customer.email_address, 'codycoder@gmail.com')
        self.assertEqual(customer.activity_status, True)
        self.assertEqual(customer.credit_limit, 10500)
        LOGGER.info('add_customer test completed')

    def test_search_customer(self):
        '''tests search_customer function'''
        customer_dict = search_customer('D123')
        expected_dict = {'first_name': 'John',
                         'last_name': 'Coder',
                         'email_address': 'johncoder@gmail.com',
                         'phone_number': 4258291234}
        self.assertEqual(customer_dict, expected_dict)
        LOGGER.info('search_customer test completed')

        # Testing for invalid customer_id in function's argument
        with self.assertRaises(ValueError):
            search_customer('D1')

    def test_delete_customer(self):
        '''tests delete_customer function'''
        customer = Customer.get(Customer.customer_id == 'D123')
        self.assertEqual(customer.email_address, 'johncoder@gmail.com')
        delete_customer('D123')
        LOGGER.info('customer deleted')
        with self.assertRaises(ValueError):
            delete_customer('D123')
        LOGGER.info('delete_customer test completed')

    def test_update_customer_credit(self):
        '''tests update_customer_credit function'''
        customer = Customer.get(Customer.customer_id == 'D123')
        LOGGER.info('Checking customer credit limit before updated')
        LOGGER.info("Customer's credit limit is %s", customer.credit_limit)
        self.assertEqual(customer.credit_limit, 10500)

        update_customer_credit('D123', 200)
        customer = Customer.get(Customer.customer_id == 'D123')
        LOGGER.info('Checking customer credit limit after update')
        LOGGER.info("Customer's credit limit is %s", customer.credit_limit)
        self.assertEqual(customer.credit_limit, 200)

        # Testing for invalid customer_id in function's argument
        with self.assertRaises(ValueError):
            update_customer_credit('D987', 500)

    def test_list_active_customers(self):
        '''tests list_active_customers function'''
        active_count = list_active_customers()
        self.assertEqual(1, active_count)

        customer = Customer.get(Customer.customer_id == 'D123')
        customer.delete_instance()
        active_count = list_active_customers()
        self.assertEqual(0, active_count)

    def test_integration(self):
        '''testing that basic_operations functions work together'''
        database.drop_tables([Customer])
        database.create_tables([Customer])

        add_customer('D123', 'John', 'Coder', '12345 High St W', 4258291234,
                     'johncoder@gmail.com', True, 10500)

        add_customer('C123', 'Cody', 'Coder', None, 4258299876,
                     'codycoder@gmail.com', False, None)

        customer_dict = search_customer('D123')
        expected_dict = {'first_name': 'John',
                         'last_name': 'Coder',
                         'email_address': 'johncoder@gmail.com',
                         'phone_number': 4258291234}
        self.assertEqual(customer_dict, expected_dict)

        active = list_active_customers()
        self.assertEqual(1, active)

        update_customer_credit('D123', 100)
        customer = Customer.get(Customer.customer_id == 'D123')
        self.assertEqual(customer.credit_limit, 100)

        delete_customer('D123')

        active = list_active_customers()
        self.assertEqual(0, active)
