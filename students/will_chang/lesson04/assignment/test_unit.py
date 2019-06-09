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

    def test_list_active_customer_names(self):
        """
        Test list_active_customer_names function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 120)
        add_customer('A15153', 'Qui-Gon',
                     'Jinn', 'Earth',
                     '100-608-1211', 'q.j@jedi.com',
                     True, 160)
        add_customer('B13400', 'Yoda',
                     'The Green One', 'Dagobah',
                     '105-718-9501', 'y.t@jedi.com',
                     True, 160)
        compare_list = ['Obi-wan', 'Qui-Gon', 'Yoda']
        self.assertEqual(list_active_customer_names(), compare_list)

    def test_filter_by_credit(self):
        """
        Test filter_by_credit function
        """
        setup()
        add_customer('A15157', 'Obi-wan',
                     'Kenobi', 'Tatooine',
                     '900-008-1111', 'o.kenobi@jedi.com',
                     True, 249)
        add_customer('A15153', 'Qui-Gon',
                     'Jinn', 'Earth',
                     '100-608-1211', 'q.j@jedi.com',
                     True, 250)
        add_customer('B13400', 'Yoda',
                     'The Green One', 'Dagobah',
                     '105-718-9501', 'y.t@jedi.com',
                     True, 251)
        compare_list_250 = ['Qui-Gon (A15153)', 'Yoda (B13400)']
        compare_list_251 = ['Yoda (B13400)']
        compare_list_252 = []
        self.assertEqual(filter_by_credit(250), compare_list_250)
        self.assertEqual(filter_by_credit(251), compare_list_251)
        self.assertEqual(filter_by_credit(252), compare_list_252)
