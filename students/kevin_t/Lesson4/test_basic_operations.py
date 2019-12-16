""" Unit testing for HP Norton Project """
from unittest import TestCase
from peewee import *
from basic_operations import Customer, add_customer, search_customer, delete_customer, update_customer_credit, list_active_customers, database

def create_database():
    database.drop_tables([Customer])
    database.create_tables([Customer])
    database.close()

class CustomerTest(TestCase):
    def test_add_customer(self):
        """ Verify that the attributes have been appropriately assigned """
        create_database()

        add_customer(1738, 'Bartholomew', 'Simpson', '742 Evergreen Terrace', 12065554682, 'Bartman99@aol.com', True, 101.50)

        test_customer = Customer.get(Customer.customer_id == 1738)
        self.assertEqual(1738, test_customer.customer_id)
        self.assertEqual('Bartholomew', test_customer.first_name)
        self.assertEqual('Simpson', test_customer.last_name)
        self.assertEqual('742 Evergreen Terrace', test_customer.home_address)
        self.assertEqual(12065554682, test_customer.phone_number)
        self.assertEqual('Bartman99@aol.com', test_customer.email_address)
        self.assertEqual(True, test_customer.status)
        self.assertEqual(101.50, test_customer.credit_limit)

    def test_search_customer(self):
        """ Verify that customers can be searched for correctly """
        create_database()
        add_customer(1738, 'Bartholomew', 'Simpson', '742 Evergreen Terrace', 12065554682, 'Bartman99@aol.com', True, 101.50)
        add_customer(1739, 'Monty', 'Burns', '1 Money Street', 12065554531, 'MoneyManMonty@aol.com', True, 1000000)

        search_result = search_customer(1738)
        correct_result = {1738: ['Bartholomew', 'Simpson', 12065554682, 'Bartman99@aol.com']}

        self.assertEqual(search_result, correct_result)

        self.assertRaises(ValueError, search_customer, 2000)

    def test_delete_customer(self):
        """ Verify that customers can be deleted correctly """
        create_database()
        add_customer(1738, 'Bartholomew', 'Simpson', '742 Evergreen Terrace', 12065554682, 'Bartman99@aol.com', True, 101.50)
        add_customer(1739, 'Monty', 'Burns', '1 Money Street', 12065554531, 'MoneyManMonty@aol.com', True, 1000000)

        delete_customer(1738)

        self.assertRaises(ValueError, search_customer, 1738)
        self.assertRaises(ValueError, delete_customer, 2000)

    def test_update_customer_credit(self):
        """ Verify that customers' credit limit can be updated correctly """
        create_database()
        add_customer(1738, 'Bartholomew', 'Simpson', '742 Evergreen Terrace', 12065554682, 'Bartman99@aol.com', True, 101.50)
        add_customer(1739, 'Monty', 'Burns', '1 Money Street', 12065554531, 'MoneyManMonty@aol.com', True, 1000000)

        update_customer_credit(1738, 200)

        updated_result = Customer.get(Customer.customer_id == 1738).credit_limit
        correct_result = 200

        self.assertEqual(updated_result, correct_result)

        self.assertRaises(ValueError, update_customer_credit, 2000, 500)

    def test_list_active_customers(self):
        """ Verify that active customers can be correctly counted """
        create_database()
        add_customer(1738, 'Bartholomew', 'Simpson', '742 Evergreen Terrace', 12065554682, 'Bartman99@aol.com', True, 101.50)
        add_customer(1739, 'Monty', 'Burns', '1 Money Street', 12065554531, 'MoneyManMonty@aol.com', True, 1000000)
        add_customer(1740, 'Seymour', 'Skinner', '44 Skid Row', 18002255288, 'MommasBoy55@aol.com', False, 21)

        query_result = list_active_customers()
        correct_result = 2
        self.assertEqual(query_result, correct_result)
