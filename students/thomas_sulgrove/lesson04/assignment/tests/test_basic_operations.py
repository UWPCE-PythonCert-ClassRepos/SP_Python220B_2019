"""tests for basic operations """

# pylint: disable=wrong-import-position
import sys

sys.path.append("..\\src")

# pylint: enable=wrong-import-position

# pylint: disable=import-error
import random
from unittest import TestCase
import peewee as pw
from basic_operations import add_customer, search_customer, \
    delete_customer, update_customer, list_active_customers
from cust_schema import Customer, DATABASE

random.randint(0, 10)


def database_setup():
    """function for setting up clean table each time"""
    DATABASE.drop_tables([Customer])
    DATABASE.create_tables([Customer])
    DATABASE.close()


TEST_CUSTOMERS = [{'id': 1, 'first_name': 'Guy', 'last_name': 'Dudeman',
                   'address': '1139 Bro Street', 'phone_number': '800-123-4567',
                   'email': 'Guy_Dudeman01@gmail.com', 'status': True,
                   'credit_limit': 1000000},

                  {'id': 2, 'first_name': 'Man', 'last_name': 'Dudeguy',
                   'address': '3729 High Five Ave', 'phone_number': '800-234-5678',
                   'email': 'Man_Guydude31@gmail.com', 'status': False,
                   'credit_limit': 37},

                  {'id': 3, 'first_name': 'Jenny', 'last_name': 'Anylady',
                   'address': '1000 Baltimore Blvd', 'phone_number': '800-867-5309',
                   'email': 'Dontchangeyournumber@gmail.com', 'status': True,
                   'credit_limit': 19035768},

                  {'id': 4, 'first_name': 'Felice', 'last_name': 'Gertrude',
                   'address': '1000 1st Street', 'phone_number': '800-000-0000',
                   'email': 'Knits4kicks@gmail.com.com', 'status': True,
                   'credit_limit': 5000},

                  {'id': 5, 'first_name': 'Walt', 'last_name': 'Kowalski',
                   'address': '238 Rhode Island Street', 'phone_number': '800-000-0001',
                   'email': 'getoffmylawn@gmail.com', 'status': False,
                   'credit_limit': 100000}
                  ]


class TestBasicOps(TestCase):
    """Class for housing the tests"""

    def test_add_customer(self):
        """Test the ability to add a customer"""
        database_setup()

        for customer in TEST_CUSTOMERS:
            add_customer(customer['id'], customer['first_name'], customer['last_name'],
                         customer['address'], customer['phone_number'], customer['email'],
                         customer['status'], customer['credit_limit'])

            test = Customer.get(Customer.customer_id == customer['id'])
            self.assertEqual(test.customer_first_name, customer['first_name'])
            self.assertEqual(test.customer_last_name, customer['last_name'])
            self.assertEqual(test.customer_home_address, customer['address'])
            self.assertEqual(test.customer_phone_number, customer['phone_number'])
            self.assertEqual(test.customer_email, customer['email'])
            self.assertEqual(test.customer_status, customer['status'])
            self.assertEqual(test.customer_credit_limit, customer['credit_limit'])

            with self.assertRaises(pw.IntegrityError):
                add_customer(customer['id'], customer['first_name'], customer['last_name'],
                             customer['address'], customer['phone_number'], customer['email'],
                             customer['status'], customer['credit_limit'])

    def test_search_customer(self):
        """Test the ability to search for a customer"""
        database_setup()

        # add in all the customers
        for customer in TEST_CUSTOMERS:
            add_customer(customer['id'], customer['first_name'], customer['last_name'],
                         customer['address'], customer['phone_number'], customer['email'],
                         customer['status'], customer['credit_limit'])

        # Loop through and see if can find all the customers
        for customer in TEST_CUSTOMERS:
            test_dict = {'Name': customer['first_name'], 'Last Name': customer['last_name'],
                         'Email': customer['email'], 'Phone Number': customer['phone_number']}

            # Test that the results match up
            self.assertEqual(search_customer(customer['id']), test_dict)

    def test_update_customer(self):
        """Test the ability to ability to update a customer"""
        database_setup()

        # add in all the customers
        for customer in TEST_CUSTOMERS:
            add_customer(customer['id'], customer['first_name'], customer['last_name'],
                         customer['address'], customer['phone_number'], customer['email'],
                         customer['status'], customer['credit_limit'])

        cust_id = None # so pylint doesnt yell at me
        for cust_id in [customer['id'] for customer in TEST_CUSTOMERS]:
            test_value = random.randint(0, 100000000)
            update_customer(cust_id, test_value)

        self.assertAlmostEqual(Customer.get(Customer.customer_id
                                            == cust_id).customer_credit_limit, test_value)
        with self.assertRaises(pw.DoesNotExist):
            update_customer(0, 1000)

    def test_list_active_customers(self):
        """Test the ability to test active customer"""
        database_setup()

        # add in all the customers
        test_int = 0  # num of active customers to test against
        for customer in TEST_CUSTOMERS:
            add_customer(customer['id'], customer['first_name'], customer['last_name'],
                         customer['address'], customer['phone_number'], customer['email'],
                         customer['status'], customer['credit_limit'])

            if customer['status']:
                test_int += 1  # increment if active

        self.assertEqual(list_active_customers(), test_int)

    def test_delete_customer(self):
        """Test the ability to delete a customer"""
        database_setup()

        # add in all the customers
        for customer in TEST_CUSTOMERS:
            add_customer(customer['id'], customer['first_name'], customer['last_name'],
                         customer['address'], customer['phone_number'], customer['email'],
                         customer['status'], customer['credit_limit'])

        for customer_id in [customer['id'] for customer in TEST_CUSTOMERS]:
            # test that the customer is there then is not
            self.assertNotEqual(search_customer(customer_id), dict())
            delete_customer(customer_id)
            self.assertEqual(search_customer(customer_id), dict())
            with self.assertRaises(pw.DoesNotExist):
                delete_customer(customer_id)
