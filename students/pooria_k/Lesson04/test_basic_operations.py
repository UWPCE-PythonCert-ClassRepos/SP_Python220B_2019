from basic_operations import *
from unittest import TestCase
import peewee



CUSTOMER_LIST = [('Andrew', 'peterson', '344 james ave' \
                  , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                  ('Wang', 'Wou', '103 spring ave', \
                   2223334456, 'wang_wou@gmail.com', False, 22000)]

expected_output = [('Andrew', 'peterson', '344 james ave' \
                            , 6308153728, 'a_peteerson@mail.com', True, 4500), \
                       ('Wang', 'Wou', '103 spring ave', \
                        2223334456, 'wang_wou@gmail.com', False, 22000)]

NAME = 0
LASTNAME = 1
ADDRESS = 2
PHONE = 3
EMAIL = 4
STATUS = 5
LIMIT = 6


def test_setup():
    """
    Function to initialize DB, create
    and add tables
    """
    DB.init('customer.db')
    DB.drop_tables([Customer])
    DB.create_tables([Customer])
    [add_customer(customer) for customer in CUSTOMER_LIST if customer is not None]

class test_basic_operations(TestCase):
    """
    This class includes all the test function
    for testing functions inside basic_operation.py
    """

    def test_add_customer(self):
        """Test adding new customer"""
        test_setup()
        customer_1_expected_output = expected_output[0]



        customer_1 = Customer.get(Customer.id == 1)

        self.assertEqual(customer_1.name, customer_1_expected_output[NAME])
        self.assertEqual(customer_1.lastname, customer_1_expected_output[LASTNAME])
        self.assertEqual(customer_1.home_address, customer_1_expected_output[ADDRESS])
        self.assertEqual(customer_1.phone_number, customer_1_expected_output[PHONE])
        self.assertEqual(customer_1.email_address, customer_1_expected_output[EMAIL])
        self.assertEqual(customer_1.status, customer_1_expected_output[STATUS])
        self.assertEqual(customer_1.credit_limit, customer_1_expected_output[LIMIT])

        expected_output_dic = {'id': 1,
                           'name': 'Andrew',
                           'last_name': 'peterson',
                           'phone_number': 6308153728,
                           'email_address': 'a_peteerson@mail.com'}
        self.assertDictEqual(search_customer(1), expected_output_dic)

    def test_adding_duplicate_add_customer(self):
        """ Test add_customer() will raise "IntegrityError"
         exception when we try to add duplicate date """
        customer_1 = ('Andrew', 'peterson', '344 james ave' \
                              , 6308153728, 'a_peteerson@mail.com', True, 4500)

        add_customer(customer_1)
        self.assertRaises(peewee.IntegrityError)



    def test_search_cutomer(self):
        """Test searching a customer"""
        test_setup()
        expected_output_1 = {'id': 1,
                           'name': 'Andrew',
                           'last_name': 'peterson',
                           'phone_number': 6308153728,
                           'email_address': 'a_peteerson@mail.com'}

        expected_output_2 = {'id': 2,
                           'name': 'Wang',
                           'last_name': 'Wou',
                           'phone_number': 2223334456,
                           'email_address': 'wang_wou@gmail.com'}

        self.assertDictEqual(search_customer(1),expected_output_1)
        self.assertDictEqual(search_customer(2), expected_output_2)


    def test_search_for_customer_that_dose_not_exists(self):
        """testing search_customer for customer ID
        That dose not exists """
        search_customer(4)
        self.assertRaises(Customer.DoesNotExist)


    def test_del_customer(self):
        """Test deleting a customer"""
        test_setup()
        del_customer(1)
        self.assertDictEqual(search_customer(1),{})

    def test_delete_customer_that_dose_not_exists(self):
        """Test deleting customer that
        dose not exists"""
        del_customer(4)
        self.assertRaises(Customer.DoesNotExist)

    def test_update_customer_credit(self):
        """Test updating customer credit limit """
        test_setup()
        update_customer_credit(1, 6500)
        update_customer_credit(2, 30000)
        customer_1 = Customer.get(Customer.id ==1)
        customer_2 = Customer.get(Customer.id ==2)
        self.assertEqual(customer_1.credit_limit, 6500)
        self.assertEqual(customer_2.credit_limit, 30000)

    def test_update_customer_credit_that_dosenot_exists(self):
        """Test updating customer credit limit
         for a customer that dose not exists """
        update_customer_credit(5, 30000)
        self.assertRaises(Customer.DoesNotExist)

    def test_list_active_customer(self):
        """testing list_active_customer()"""
        test_setup()
        self.assertEqual(list_active_customers(), 1)

    def test_query_all_customers(self):
        """ testing query_all_customers(),
            Generator to return customer_id for all the
            customers int the DB"""
        test_setup()
        expected_output_list = [{'id': 1, 'name': 'Andrew', 'last_name': 'peterson',\
                        'phone_number': 6308153728, 'email_address': 'a_peteerson@mail.com'}\
                         , {'id': 2, 'name': 'Wang', 'last_name': 'Wou', 'phone_number': 2223334456,\
                         'email_address': 'wang_wou@gmail.com'}]
        self.assertEqual(query_all_customers(), expected_output_list)


    def test_db_init(self):
        db_init()
        customer_1_expected_output = expected_output[0]
        customer_1 = Customer.get(Customer.id == 1)

        self.assertEqual(customer_1.name, customer_1_expected_output[NAME])
        self.assertEqual(customer_1.lastname, customer_1_expected_output[LASTNAME])
        self.assertEqual(customer_1.home_address, customer_1_expected_output[ADDRESS])
        self.assertEqual(customer_1.phone_number, customer_1_expected_output[PHONE])
        self.assertEqual(customer_1.email_address, customer_1_expected_output[EMAIL])
        self.assertEqual(customer_1.status, customer_1_expected_output[STATUS])
        self.assertEqual(customer_1.credit_limit, customer_1_expected_output[LIMIT])

