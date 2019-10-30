"""
    Integration test of all the functions, just meant to put the basic operations together and make
    sure that no random errors pop up. Lets see what we get.
"""

import unittest
import logging
import sys
sys.path.append('../src')

import basic_operations as ba
from customer_model import Customer, database

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class ModuleTests(unittest.TestCase):
    """Contains our single function for integration testing."""

    def setUp(self):
        database.create_tables([Customer])

    def tearDown(self):
        Customer.delete().execute()
        database.close()

    def test_integration(self):
        """
            Test the following all together
            -add new customers to the database
            -search customers in the database
            -delete existing customers from the database
            -update customers credit
            -list the number of active customers in the database
        """

        # add a couple users all active
        ba.add_customer(1, 'Fran', 'K', '100 New York Ave, NYC, 98109', '248-331-6243',
                        'my_email@gmail.com', 'Active', 1000)

        ba.add_customer(2, 'Emily', 'H', '200 New York Ave, MA, 98109', '248-331-6243',
                       'my_email@gmail.com', 'Active', 2000)

        ba.add_customer(3, 'John', 'H', '300 New York Ave, MA, 98109', '248-331-6243',
                        'my_email@gmail.com', 'Active', 3000)

        # check the credit limit for an added user
        customer_1 = Customer.get(Customer.customer_id == 1)
        self.assertEqual(customer_1.credit_limit, 1000)

        # update the credit limit for a user and search for that user
        customer_3 = ba.search_customer(3)
        self.assertEqual(customer_3['credit_limit'], 3000)

        ba.update_customer_credit(3, 3333)
        customer_3 = ba.search_customer(3)
        self.assertEqual(customer_3['credit_limit'], 3333)

        # add a couple more users some active some not
        ba.add_customer(4, 'John', 'H', '300 New York Ave, MA, 98109', '248-331-6243',
                        'my_email@gmail.com', 'Inative', 4000)

        ba.add_customer(5, 'John', 'H', '300 New York Ave, MA, 98109', '248-331-6243',
                        'my_email@gmail.com', 'Inactive', 5000)

        ba.add_customer(6, 'John', 'H', '300 New York Ave, MA, 98109', '248-331-6243',
                        'my_email@gmail.com', 'Active', 6000)

        # add an existing customer, should throw out a warning
        ba.add_customer(3, 'John', 'H', '300 New York Ave, MA, 98109', '248-331-6243',
                        'my_email@gmail.com', 'Active', 3000)

        # check how many active users we have
        active_users = ba.list_active_customers()
        self.assertEqual(active_users, 4)

        # delete all our active users
        ba.delete_customer(1)
        ba.delete_customer(2)
        ba.delete_customer(3)
        ba.delete_customer(6)

        # ensure we don't have any active users left
        active_users_2 = ba.list_active_customers()
        self.assertEqual(active_users_2, 0)
