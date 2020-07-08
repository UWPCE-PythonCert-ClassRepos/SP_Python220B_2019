""" Unit test for this project """

from unittest import TestCase
import basic_operations
from customer_model import Customer

CUSTOMER_1 = {
    'customer_id': 1,
    'customer_name': 'Steve',
    'customer_lastname': 'Jobs',
    'customer_address': 'One Infinite Loop, Cupertino, CA 95014',
    'customer_phone_number': '800-275-2273',
    'customer_email': 'steve@apple.com',
    'status': True,
    'credit_limit': 35000.00
}

CUSTOMER_2 = {
    'customer_id': 2,
    'customer_name': 'Bill',
    'customer_lastname': 'Gates',
    'customer_address': '440 5th Ave N., Seattle, WA 98109',
    'customer_phone_number': '206-709-3100 ext. 7100',
    'customer_email': 'bill.gates@gatesfoundation.org',
    'status': True,
    'credit_limit': 62500.00
}

CUSTOMER_3 = {
    'customer_id': 3,
    'customer_name': 'Mark',
    'customer_lastname': 'Zuckerberg',
    'customer_address': '1 Hacker Way, Menlo Park, California 94025',
    'customer_phone_number': None,
    'customer_email': 'mz@fb.com',
    'status': True,
    'credit_limit': 25500.00
}

class BasicOperationsTest(TestCase):
    """ unit test for basic_operations """
    def add_customers(self):
        """ add customers to database for testing """
        basic_operations.add_customer(CUSTOMER_1['customer_id'],
                                      CUSTOMER_1['customer_name'],
                                      CUSTOMER_1['customer_lastname'],
                                      CUSTOMER_1['customer_address'],
                                      CUSTOMER_1['customer_phone_number'],
                                      CUSTOMER_1['customer_email'],
                                      CUSTOMER_1['status'],
                                      CUSTOMER_1['credit_limit']
                                     )

        basic_operations.add_customer(CUSTOMER_2['customer_id'],
                                      CUSTOMER_2['customer_name'],
                                      CUSTOMER_2['customer_lastname'],
                                      CUSTOMER_2['customer_address'],
                                      CUSTOMER_2['customer_phone_number'],
                                      CUSTOMER_2['customer_email'],
                                      CUSTOMER_2['status'],
                                      CUSTOMER_2['credit_limit']
                                     )

        basic_operations.add_customer(CUSTOMER_3['customer_id'],
                                      CUSTOMER_3['customer_name'],
                                      CUSTOMER_3['customer_lastname'],
                                      CUSTOMER_3['customer_address'],
                                      CUSTOMER_3['customer_phone_number'],
                                      CUSTOMER_3['customer_email'],
                                      CUSTOMER_3['status'],
                                      CUSTOMER_3['credit_limit']
                                     )

    def delete_customers(self):
        """ delete customers from database for testing """
        basic_operations.delete_customer(1)
        basic_operations.delete_customer(2)
        basic_operations.delete_customer(3)

    def test_add_customer(self):
        """ unit test for adding cutomers to the database """
        # set up
        self.add_customers()

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

        # clean up
        self.delete_customers()

    def test_add_customer_existing(self):
        """ unit test for adding cutomers to the database """
        # set up
        self.add_customers()

        try:
            basic_operations.add_customer(CUSTOMER_3['customer_id'],
                                        CUSTOMER_3['customer_name'],
                                        CUSTOMER_3['customer_lastname'],
                                        CUSTOMER_3['customer_address'],
                                        CUSTOMER_3['customer_phone_number'],
                                        CUSTOMER_3['customer_email'],
                                        CUSTOMER_3['status'],
                                        CUSTOMER_3['credit_limit']
                                        )
        except Exception as err:
            self.fail(err)

        # clean up
        self.delete_customers()

    def test_search_customer(self):
        """ unit test for searching for cutomers in the database """
        # set up
        self.add_customers()

        db_customer_1 = basic_operations.search_customer(1)
        db_customer_2 = basic_operations.search_customer(2)
        db_customer_3 = basic_operations.search_customer(3)

        self.assertDictEqual(CUSTOMER_1, db_customer_1)
        self.assertDictEqual(CUSTOMER_2, db_customer_2)
        self.assertDictEqual(CUSTOMER_3, db_customer_3)

        # clean up
        self.delete_customers()

    def test_update_credit_limit(self):
        """ unit test for updating the cutomer's credit limit to the database """
        # set up
        self.add_customers()

        credit_limit_1 = 50000.00
        credit_limit_2 = 150000.00
        credit_limit_3 = 250000.00

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

        # clean up
        self.delete_customers()

    def test_list_active_customers(self):
        """ unit test for getting the number of active customers """
        # set up
        self.add_customers()

        self.assertEqual(3, basic_operations.list_active_customers())
        self.assertNotEqual(0, basic_operations.list_active_customers())

        # clean up
        self.delete_customers()

    def test_delete_customer(self):
        """ unit test for deleting cutomers from the database """
        # set up
        self.add_customers()

        self.delete_customers()

        db_customer_1 = basic_operations.search_customer(1)
        db_customer_2 = basic_operations.search_customer(2)
        db_customer_3 = basic_operations.search_customer(3)

        self.assertEqual({}, db_customer_1)
        self.assertEqual({}, db_customer_2)
        self.assertEqual({}, db_customer_3)

        self.assertNotEqual(CUSTOMER_1, db_customer_1)
        self.assertNotEqual(CUSTOMER_2, db_customer_2)
        self.assertNotEqual(CUSTOMER_3, db_customer_3)
'''

'''
