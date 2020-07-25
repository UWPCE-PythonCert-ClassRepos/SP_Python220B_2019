"""Basic Operation Unit Tests"""
import sys
sys.path.append('../')
from unittest import TestCase
import basic_operations
from customer_model import Customer, database


CUSTOMER_ID = 0
CUSTOMER_NAME = 1
CUSTOMER_LASTNAME = 2
CUSTOMER_HOME_ADDRESS = 3
CUSTOMER_PHONE_NUMNER = 4
CUSTOMER_EMAIL_ADDRESS = 5
CUSTOMER_STATUS = 6
CUSTOMER_CREDIT_LIMIT = 7

customers = [('1', 'Damien', 'Liilard', '456 Point Guard Ln', '503-555-1234', 'dlillard@trailblazers.com', True, 100000.00),
             ('2', 'CJ', 'McCollum', '308 Pinot Noir Rd', '503-555-9876', 'winesnob@trailblazers.com', True, 50000.00),
             ('3', 'Greg', 'Oden', '543 Bad Luck Heights', '808-555-9696', 'what@couldhavebeen.com', False, 100.00)]

pp_customers = ['Cust ID#1     Damien Liilard                 Ph: 503-555-1234, Address: 456 Point Guard Ln            , Active:Yes, Limit:     100000',
                'Cust ID#2     CJ McCollum                    Ph: 503-555-9876, Address: 308 Pinot Noir Rd             , Active:Yes, Limit:      50000',
                'Cust ID#3     Greg Oden                      Ph: 808-555-9696, Address: 543 Bad Luck Heights          , Active:No , Limit:        100']

new_customers = [('4', 'Zach', 'Collins', '78 Shoulder Pain', '503-555-9999', 'zcollins@trailblazers.com', True, 1995.00)]


class BasicOperationsTest(TestCase):
    def setUp(self):
        database.drop_tables([Customer])
        database.create_tables([Customer])
        for customer in customers:
            Customer.create(customer_id=customer[CUSTOMER_ID],
                            name=customer[CUSTOMER_NAME],
                            lastname=customer[CUSTOMER_LASTNAME],
                            home_address=customer[CUSTOMER_HOME_ADDRESS],
                            phone_number=customer[CUSTOMER_PHONE_NUMNER],
                            email_address=customer[CUSTOMER_EMAIL_ADDRESS],
                            status=customer[CUSTOMER_STATUS],
                            credit_limit=customer[CUSTOMER_CREDIT_LIMIT])


    """Basic Operation Unit Tests"""
    def test_add_customer(self):
        test_customer = new_customers[0]
        new_customer = basic_operations.add_customer(test_customer[0],
                                                     test_customer[1],
                                                     test_customer[2],
                                                     test_customer[3],
                                                     test_customer[4],
                                                     test_customer[5],
                                                     test_customer[6],
                                                     test_customer[7])

        self.assertEqual(new_customer.customer_id, test_customer[0])
        self.assertEqual(new_customer.name, test_customer[1])
        self.assertEqual(new_customer.lastname, test_customer[2])
        self.assertEqual(new_customer.home_address, test_customer[3])
        self.assertEqual(new_customer.phone_number, test_customer[4])
        self.assertEqual(new_customer.email_address, test_customer[5])
        self.assertEqual(new_customer.status, test_customer[6])
        self.assertEqual(new_customer.credit_limit, test_customer[7])

    def test_search_customer(self):
        expected = customers[0]
        customer = basic_operations.search_customer('1')
        self.assertEqual(customer.customer_id, expected[0])
        self.assertEqual(customer.name, expected[1])
        self.assertEqual(customer.lastname, expected[2])
        self.assertEqual(customer.home_address, expected[3])
        self.assertEqual(customer.phone_number, expected[4])
        self.assertEqual(customer.email_address, expected[5])
        self.assertEqual(customer.status, expected[6])
        self.assertEqual(customer.credit_limit, expected[7])

    def test_search_customer_does_not_exist(self):

        customer = basic_operations.search_customer('5')
        self.assertEqual(customer, None)

    def test_delete_customer(self):
        expected = customers[0]
        self.assertTrue(basic_operations.delete_customer(expected[CUSTOMER_ID]))

    def test_delete_customer_does_not_exist(self):
        self.assertFalse(basic_operations.delete_customer('5'))

    def test_update_customer(self):
        cust = basic_operations.update_customer_credit('1', 250.00)
        self.assertEqual(cust.credit_limit, 250.00)

    def test_update_customer_not_exist(self):
        cust = basic_operations.update_customer_credit('5', 500.00)
        self.assertEqual(cust, None)

    def test_list_active_customers(self):
        self.assertEqual(basic_operations.list_active_customers(), 2)

    def test_list_all_customers(self):
        self.assertEqual(basic_operations.list_all_customers(), pp_customers)

