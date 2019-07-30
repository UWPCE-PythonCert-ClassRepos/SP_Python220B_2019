from unittest import TestCase
from basic_operations import *
from customer_model import *


def set_up():
    """
   populate database
    """

    DATABASE.drop_tables([Customer])
    DATABASE.create_tables([Customer])
    DATABASE.close()


class BasicOperationsTests(TestCase):

    def test_add_customer(self):
        """
        Test add_customer
        :return: None
        """

        set_up()
        customer = (1, 'Amy', 'Walker', 'Washington', '12345',
                    'amywalker@gmail.com', True, 750)
        add_customer(*customer)
        a_customer = Customer.get(Customer.customer_id == 1)

        self.assertEqual(a_customer.customer_id, 1)
        self.assertEqual(a_customer.first_name, 'Amy')
        self.assertEqual(a_customer.last_name, 'Walker')
        self.assertEqual(a_customer.home_address, 'Washington')
        self.assertEqual(a_customer.phone_number, '12345')
        self.assertEqual(a_customer.is_active, True)
        self.assertEqual(a_customer.email_address, 'amywalker@gmail.com')
        self.assertEqual(a_customer.credit_limit, 750)

    def test_search_customer(self):
        """
        Test search_customer
        :return: None
        """
        set_up()
        customer = (1, 'Amy', 'Walker', 'Washington', '12345',
                    'amywalker@gmail.com', True, 750)
        add_customer(*customer)
        actual = search_customer(1)
        expected = {'first_name': 'Amy', 'last_name': 'Walker',
                    'email_address': 'amywalker@gmail.com',
                    'phone_number': '12345'}
        self.assertEqual(actual, expected)

    def test_delete_customer(self):
        """
        Test delete_customer
        :return: None
        """
        set_up()
        customer = (1, 'Amy', 'Walker', 'Washington', '12345',
                    'amywalker@gmail.com', True, 750)
        add_customer(*customer)
        delete_customer(1)


    def test_update_customer_credit(self):
        """
        Test update_customer_credit
        :return: None
        """
        set_up()
        customer = (1, 'Amy', 'Walker', 'Washington', '12345',
                    'amywalker@gmail.com', True, 750)
        add_customer(*customer)
        a_customer = Customer.get(Customer.customer_id == 1)
        update_customer_credit(1, 750)
        self.assertEqual(a_customer.credit_limit, 750)

        with self.assertRaises(ValueError):
            update_customer_credit(2, 500)


    def test_list_active_customer(self):
        """
        Test list_active_customer
        :return: None
        """
        set_up()
        customer = (1, 'Amy', 'Walker', 'Washington', '12345',
                    'amywalker@gmail.com', True, 750)
        add_customer(*customer)
        self.assertEqual(list_active_customer(), 1)
