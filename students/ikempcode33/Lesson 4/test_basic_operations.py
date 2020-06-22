"""Tests customer model operations"""
import logging
from customer_model import *
from basic_operations import *
from unittest import TestCase

#Set up logging info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("logger is active_")


class TestBasicOp(TestCase):
    logger.info("testing basic operations")

    def setUp(self):
        #used to create database tables and set up the test customers data
        logger.info('creating tables')
        database.drop_tables([Customer])
        database.create_tables([Customer])
        logger.info('tables are created.')

        logger.info('Adding data to database')
        # Test customer 1
        add_customer(1773, 'Karen', 'Smith',
                     '142 42 st, Bellevue, WA 98105',
                     '123-456-7890', 'ksmith99@gmail.com',
                     True, 40000.00)
        # Test customer 2
        add_customer(1223, 'Georgia', 'Smith',
                     '123 5 st, Palmsprings, CA 94930',
                     '415-890-8787', 'gsmith@gmail.com',
                     True, 60000.00)
        # Test customer 3
        add_customer(1003, 'Paul', 'Stevens',
                     '773 7 st, Los Angeles, CA 90005',
                     '415-770-3434', 'pstevens199@gmail.com',
                     True, 50000.00)
        logger.info("data is uploaded, ready to begin tests")

    def test_add_customer(self):
        """Tests that adding a customer to database works"""
        cus_1 = Customer.get(Customer.customer_id == 1773)
        self.assertEqual(cus_1.customer_id, 1773)
        self.assertEqual(cus_1.first_name, 'Karen')
        self.assertEqual(cus_1.last_name, 'Smith')
        self.assertEqual(cus_1.home_address, '142 42 st, Bellevue, WA 98105')
        self.assertEqual(cus_1.phone_number, '123-456-7890')
        self.assertEqual(cus_1.status, True)
        self.assertEqual(cus_1.credit_limit, 40000.00)

    def test_add_customers(self):
        """Tests that adding multiple customers to database works"""
        new_cus1 = (9887, 'Bell', 'Andrews',
                   '83 4 st, Seattle, WA 98105',
                   '143-455-7000', 'bandrews@gmail.com',
                   True, 8000.00)
        new_cus2 = (3344, 'Drew', 'Simons',
                   '313 5 st, Olympia, WA 90087',
                   '145-677-8925', 'dsimons@gmail.com',
                   True, 9000.00)
        new_cus3 = (8882, 'Henry', 'Kemp',
                   '89 6 st, New York City, NY 70095',
                   '148-495-7900', 'hkemp@gmail.com',
                   True, 5000.00)
        add_customers([new_cus1, new_cus2, new_cus3])

        cus1 = Customer.get(Customer.customer_id == 9887)
        cus2 = Customer.get(Customer.customer_id == 3344)
        cus3 = Customer.get(Customer.customer_id == 8882)
        self.assertEqual(cus1.first_name, 'Bell')
        self.assertEqual(cus1.credit_limit, 8000.00)
        self.assertEqual(cus2.first_name, 'Drew')
        self.assertEqual(cus2.credit_limit, 9000.00)
        self.assertEqual(cus3.first_name, 'Henry')
        self.assertEqual(cus3.credit_limit, 5000.00)

    def test_search_customer(self):
        """Tests that a customer can be searched via ID"""
        cus_2 = search_customer(1003)
        logger.info("searching for customer ID 1003")
        expected = {'first_name': 'Paul',
                    'last_name': 'Stevens',
                    'phone_number': '415-770-3434',
                    'email_address': 'pstevens199@gmail.com'}
        self.assertEqual(cus_2, expected)
    
    def test_invalid_customer_id(self):
        """If there is an unknown ID this tests that an empty object returned"""
        cus_1 = search_customer(123232)
        self.assertEqual(cus_1, {})

    def test_update_customer_credit(self):
        """Tests that customers credit can be updated"""
        update_customer_credit(1773, 60000)
        cus_1 = Customer.get(Customer.customer_id == 1773).credit_limit
        self.assertEqual(cus_1, 60000)

        with self.assertRaises(DoesNotExist):
            update_customer_credit(3334, 10000)

    def test_list_active_customers(self):
        """Test if active customer function works"""
        num = list_active_customers()
        self.assertEqual(num, 3)
    
    def test_delete_customer(self):
        delete_customer(1773)
        expected = search_customer(1773)
        self.assertEqual(expected, {})
        with self.assertRaises(DoesNotExist):
            delete_customer(3334)

