"""Unit test for basic operations program"""
# pylint: disable= W0401,W1202
from unittest import TestCase
from HP import *
from basic_operations import add_customer, search_customer, delete_customer
from basic_operations import update_customer_credit, list_active_customers
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


# create a set of customers


def drop_db():
    """Drops customer table"""
    database.drop_tables([Customer])
    database.close()


def create_empty_db():
    """Creates an empty customer database"""
    drop_db()
    database.create_tables([Customer])
    database.close()


class BasicOperationsTest(TestCase):
    """Tests basic_operations program, along with customer_model"""

    def test_add_customer(self):
        """Tests if a new customer is added to database"""
        customer_1 = {'customer_id': '0000', 'name': 'Victor', 'last_name': 'Medina',
                      'home_address': '809 Newton ave', 'phone_number': '5165996074',
                      'email_address': 'vmedina1014@gmail.com', 'status': True,
                      'credit_limit': 800}
        create_empty_db()
        add_customer(**customer_1)
        query = Customer.get(Customer.customer_id == customer_1['customer_id'])
        self.assertEqual(customer_1['name'], query.customer_name)
        self.assertEqual(customer_1['last_name'], query.customer_last_name)
        self.assertEqual(customer_1['home_address'], query.home_address)
        self.assertEqual(customer_1['phone_number'], query.phone_number)
        self.assertEqual(customer_1['email_address'], query.email_address)
        self.assertEqual(customer_1['status'], bool(query.status))
        self.assertEqual(customer_1['credit_limit'], query.credit_limit)

        customer_2 = {'customer_id': '9860', 'name': 'Roger', 'last_name': 'Fortune',
                      'home_address': '676 Grand ave', 'phone_number': '5165946824',
                      'email_address': 'fortune_roger676@gmail.com', 'status': True,
                      'credit_limit': 750}

        add_customer(**customer_2)
        query = Customer.get(Customer.customer_id == customer_2['customer_id'])
        self.assertEqual(customer_2['name'], query.customer_name)
        self.assertEqual(customer_2['last_name'], query.customer_last_name)
        self.assertEqual(customer_2['home_address'], query.home_address)
        self.assertEqual(customer_2['phone_number'], query.phone_number)
        self.assertEqual(customer_2['email_address'], query.email_address)
        self.assertEqual(customer_2['status'], bool(query.status))
        self.assertEqual(customer_2['credit_limit'], query.credit_limit)

    def test_search_customer(self):
        create_empty_db()

        customer_1 = {'customer_id': '0000', 'name': 'Victor', 'last_name': 'Medina',
                      'home_address': '809 Newton ave', 'phone_number': '5165996074',
                      'email_address': 'vmedina1014@gmail.com', 'status': True,
                      'credit_limit': 800}
        add_customer(**customer_1)
        test_search_customer_dict = {'name': customer_1['name'], 'last_name': customer_1['last_name'],
                                     'email_address': customer_1['email_address'],
                                     'phone_number': customer_1['phone_number']}
        self.assertEqual(test_search_customer_dict, search_customer(customer_1['customer_id']))

    def test_delete_customer(self):
        create_empty_db()

        customer_1 = {'customer_id': '0000', 'name': 'Victor', 'last_name': 'Medina',
                      'home_address': '809 Newton ave', 'phone_number': '5165996074',
                      'email_address': 'vmedina1014@gmail.com', 'status': True,
                      'credit_limit': 800}
        customer_2 = {'customer_id': '9860', 'name': 'Roger', 'last_name': 'Fortune',
                      'home_address': '676 Grand ave', 'phone_number': '5165946824',
                      'email_address': 'fortune_roger676@gmail.com', 'status': True,
                      'credit_limit': 750}
        add_customer(**customer_1)
        add_customer(**customer_2)
        delete_customer(customer_1['customer_id'])
        search_customer(customer_1['customer_id'])
        self.assertEqual({}, search_customer(customer_1['customer_id']))

    def test_update_customer_credit(self):
        create_empty_db()
        customer_1 = {'customer_id': '0000', 'name': 'Victor', 'last_name': 'Medina',
                      'home_address': '809 Newton ave', 'phone_number': '5165996074',
                      'email_address': 'vmedina1014@gmail.com', 'status': True,
                      'credit_limit': 800}
        add_customer(**customer_1)

        update_customer_credit(customer_1['customer_id'], 1000)
        query = Customer.get(Customer.customer_id == customer_1['customer_id'])
        self.assertEqual(query.credit_limit, 1000)

    def test_list_active_customers(self):
        """
        :return:
        :rtype:
        """
        create_empty_db()
        customer_1 = {'customer_id': '0000', 'name': 'Victor', 'last_name': 'Medina',
                      'home_address': '809 Newton ave', 'phone_number': '5165996074',
                      'email_address': 'vmedina1014@gmail.com', 'status': True,
                      'credit_limit': 800}
        customer_2 = {'customer_id': '9860', 'name': 'Roger', 'last_name': 'Fortune',
                      'home_address': '676 Grand ave', 'phone_number': '5165946824',
                      'email_address': 'fortune_roger676@gmail.com', 'status': True,
                      'credit_limit': 750}
        add_customer(**customer_1)
        add_customer(**customer_2)
        self.assertEqual(2,list_active_customers())