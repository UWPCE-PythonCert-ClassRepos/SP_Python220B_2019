"""
Unit Tests for basic_operations.py
"""

from unittest import TestCase
from peewee import *
from basic_operations import *
from customer_model import *


def setup():
    """
    Initialize database
    """

    database.drop_tables([Customer])
    database.create_tables([Customer])
    database.close()

class BasicOperationsTests(TestCase):
    """
    Contains test functions to evaluate basic_operations
    """
    def test_add_customer(self):
        """
        Test add_customer function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 120)
        acustomer = Customer.get(Customer.customer_id == 'A15157')

        self.assertEqual(acustomer.name, 'Obi-wan')
        self.assertEqual(acustomer.email_address, 'o.kenobi@jedi.com')

    def test_add_customer_fail(self):
        """
        Test add_customer function failed case
        """
        setup()
        with self.assertRaises(TypeError):
            add_customer('Not enough inputs')

    def test_search_customer(self):
        """
        Test search_customer function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 120)
        cust_dict = search_customer('A15157')
        self.assertEqual(cust_dict['lastname'], 'Kenobi')
        self.assertEqual(cust_dict['phone_number'], '900-008-1111')

    def test_delete_customer(self):
        """
        Test delete_customer function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 120)
        delete_customer('A15157')
        cust_dict = search_customer('A15157')
        self.assertEqual(cust_dict, {})

    def test_delete_customer_fail(self):
        """
        Test delete_customer function failed case
        """
        setup()
        with self.assertRaises(ValueError):
            delete_customer('A15157')

    def test_update_customer_credit(self):
        """
        Test update_customer function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 120)
        update_customer_credit('A15157', 250)
        acustomer = Customer.get(Customer.customer_id == 'A15157')
        self.assertEqual(acustomer.credit_limit, 250)

    def test_update_customer_credit_fail(self):
        """
        Test update_customer function failed case
        """
        setup()
        with self.assertRaises(ValueError):
            update_customer_credit('A15157', 250)


    def test_list_active_customers(self):
        """
        Test list_active_customers function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 120)
        self.assertEqual(list_active_customers(), 1)
        add_customer('A15153', 'Qui-Gon',
                     'Jinn', 'Earth',
                     '100-608-1211', 'q.j@jedi.com',
                     True, 160)
        self.assertEqual(list_active_customers(), 2)
