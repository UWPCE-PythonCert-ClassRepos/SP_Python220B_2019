""" Unit test for this project """

from unittest import TestCase
import basic_operations
from .customer_model import Customer

CUSTOMER_1 = {
    'customer_id': 1,
    'customer_name': 'Steve',
    'customer_lastname': 'Jobs',
    'customer_address': 'One Infinite Loop, Cupertino, CA 95014',
    'customer_phone_number': '800-275-2273',
    'customer_email': 'steve@apple.com',
    'credit_limit': 1000000,
    'status': True
}

CUSTOMER_2 = {
    'customer_id': 2,
    'customer_name': 'Bill',
    'customer_lastname': 'Gates',
    'customer_address': '440 5th Ave N., Seattle, WA 98109',
    'customer_phone_number': '206-709-3100 ext. 7100',
    'customer_email': 'bill.gates@gatesfoundation.org',
    'credit_limit': 6000000,
    'status': True
}

CUSTOMER_3 = {
    'customer_id': 3,
    'customer_name': 'Mark',
    'customer_lastname': 'Zuckerberg',
    'customer_address': '1 Hacker Way, Menlo Park, California 94025',
    'customer_phone_number': None,
    'customer_email': 'mz@fb.com',
    'credit_limit': 2500000,
    'status': True
}

class BasicOperationsTest(TestCase):
    """ unit test for basic_operations """
    def test_add_customer(self):
        """ unit test for adding cutomers to the database """
        basic_operations.add_customer(CUSTOMER_1['customer_id'],
                                      CUSTOMER_1['customer_name'],
                                      CUSTOMER_1['customer_lastname'],
                                      CUSTOMER_1['customer_address'],
                                      CUSTOMER_1['customer_phone_number'],
                                      CUSTOMER_1['customer_email'],
                                      CUSTOMER_1['credit_limit'],
                                      CUSTOMER_1['status']
                                     )

        basic_operations.add_customer(CUSTOMER_2['customer_id'],
                                      CUSTOMER_2['customer_name'],
                                      CUSTOMER_2['customer_lastname'],
                                      CUSTOMER_2['customer_address'],
                                      CUSTOMER_2['customer_phone_number'],
                                      CUSTOMER_2['customer_email'],
                                      CUSTOMER_2['credit_limit'],
                                      CUSTOMER_2['status']
                                     )

        basic_operations.add_customer(CUSTOMER_3['customer_id'],
                                      CUSTOMER_3['customer_name'],
                                      CUSTOMER_3['customer_lastname'],
                                      CUSTOMER_3['customer_address'],
                                      CUSTOMER_3['customer_phone_number'],
                                      CUSTOMER_3['customer_email'],
                                      CUSTOMER_3['credit_limit'],
                                      CUSTOMER_3['status']
                                     )

        db_customer_1 = Customer.get(Customer.customer_id == 1)
        db_customer_2 = Customer.get(Customer.customer_id == 2)
        db_customer_3 = Customer.get(Customer.customer_id == 3)

        self.assertEqual(CUSTOMER_1['customer_name'], db_customer_1.customer_name)
        self.assertEqual(CUSTOMER_2['customer_name'], db_customer_2.customer_name)
        self.assertEqual(CUSTOMER_3['customer_name'], db_customer_3.customer_name)

        self.assertEqual(CUSTOMER_1['customer_lastname'], db_customer_1.customer_lastname)
        self.assertEqual(CUSTOMER_2['customer_lastname'], db_customer_2.customer_lastname)
        self.assertEqual(CUSTOMER_3['customer_lastname'], db_customer_3.customer_lastname)

        self.assertEqual(CUSTOMER_1['customer_address'], db_customer_1.customer_address)
        self.assertEqual(CUSTOMER_2['customer_address'], db_customer_2.customer_address)
        self.assertEqual(CUSTOMER_3['customer_address'], db_customer_3.customer_address)

        self.assertEqual(CUSTOMER_1['customer_phone_number'], db_customer_1.customer_phone_number)
        self.assertEqual(CUSTOMER_2['customer_phone_number'], db_customer_2.customer_phone_number)
        self.assertEqual(CUSTOMER_3['customer_phone_number'], db_customer_3.customer_phone_number)

        self.assertEqual(CUSTOMER_1['customer_email'], db_customer_1.customer_email)
        self.assertEqual(CUSTOMER_2['customer_email'], db_customer_2.customer_email)
        self.assertEqual(CUSTOMER_3['customer_email'], db_customer_3.customer_email)

        self.assertEqual(CUSTOMER_1['credit_limit'], db_customer_1.credit_limit)
        self.assertEqual(CUSTOMER_2['credit_limit'], db_customer_2.credit_limit)
        self.assertEqual(CUSTOMER_3['credit_limit'], db_customer_3.credit_limit)

        self.assertEqual(CUSTOMER_1['status'], db_customer_1.status)
        self.assertEqual(CUSTOMER_2['status'], db_customer_2.status)
        self.assertEqual(CUSTOMER_3['status'], db_customer_3.status)

    def test_search_customer(self):
        """ unit test for searching for cutomers in the database """
        db_customer_1 = basic_operations.search_customer(1)
        self.assertEqual(CUSTOMER_1, db_customer_1)

        db_customer_2 = basic_operations.search_customer(2)
        self.assertEqual(CUSTOMER_2, db_customer_2)

        db_customer_3 = basic_operations.search_customer(3)
        self.assertEqual(CUSTOMER_3, db_customer_3)

    def test_update_credit_limit(self):
        """ unit test for updating the cutomer's credit limit to the database """
        credit_limit_1 = 5000000
        credit_limit_2 = 15000000
        credit_limit_3 = 25000000

        basic_operations.update_customer_credit(1, credit_limit_1)
        basic_operations.update_customer_credit(2, credit_limit_2)
        basic_operations.update_customer_credit(3, credit_limit_3)

        db_customer_1 = Customer.get(Customer.customer_id == 1)
        db_customer_2 = Customer.get(Customer.customer_id == 2)
        db_customer_3 = Customer.get(Customer.customer_id == 3)

        self.assertEqual(db_customer_1.credit_limit, credit_limit_1)
        self.assertEqual(db_customer_2.credit_limit, credit_limit_2)
        self.assertEqual(db_customer_3.credit_limit, credit_limit_3)

        self.assertNotEqual(db_customer_1.credit_limit, CUSTOMER_1['credit_limit'])
        self.assertNotEqual(db_customer_2.credit_limit, CUSTOMER_2['credit_limit'])
        self.assertNotEqual(db_customer_3.credit_limit, CUSTOMER_3['credit_limit'])

    def test_list_active_customers(self):
        """ unit test for getting the number of active customers """
        self.assertEqual(3, basic_operations.list_active_customers())

    def test_delete_customer(self):
        """ unit test for deleting cutomers from the database """
        basic_operations.delete_customer(1)
        basic_operations.delete_customer(2)
        basic_operations.delete_customer(3)

        db_customer_1 = basic_operations.search_customer(1)
        db_customer_2 = basic_operations.search_customer(2)
        db_customer_3 = basic_operations.search_customer(3)

        self.assertEqual({}, db_customer_1)
        self.assertEqual({}, db_customer_2)
        self.assertEqual({}, db_customer_3)
