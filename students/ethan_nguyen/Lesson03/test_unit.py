from unittest import TestCase
from unittest.mock import patch
import pytest

import basic_operations


gold = {'id': 1, 'name': 'Michael', 'last_name': 'Jordan', 'home_address': '3421 S Bull \
Street North Carolina', 'phone_number': '203-231-3223',
        'email': 'goat_test@gmail.com', 'status': 'Active',
        'credit_limit': 212109}


class CustomerDBTests(TestCase):

    def create_database(self):
        self.assertIsNotNone(basic_operations.DATABASE)

    def create_table(self):
        self.assertIsNotNone(basic_operations.Customer)

    def test_add_customer(self):

        basic_operations.delete_all_customers()

        basic_operations.add_customer(1, 'Michael', 'Jordan', '3421 S Bull Street \
North Carolina', '203-231-3223', 'goat_test@gmail.com', 'Active', 212109)

        customer = basic_operations.search_customer(1)
        self.assertDictEqual(gold, customer)

    # def test_search_customer(self):

    #     customer = basic_operations.search_customer('1')
    #     self.assertDictEqual(gold, customer)

    def test_list_active_customers(self):

        basic_operations.delete_all_customers()

        basic_operations.add_customer(2, 'Shawn', 'Kemp', '3423 Green Lake \
Street Seattle WA', '206-240-4023', 'dunk_test@gmail.com', 'Active', 212109)

        count = basic_operations.list_active_customers()
        self.assertEqual(1, count)

    def test_update_customer_credit(self):
        basic_operations.update_customer_credit(2, 200)
        customer = basic_operations.search_customer(2)
        self.assertEqual(200, customer['credit_limit'])

    def test_update_customer_credit_not_found(self):
        try:
            basic_operations.update_customer_credit(10, 300)
        except ValueError:
            self.assertRaises(ValueError)


    @pytest.mark.last
    def test_delete_customer(self):

        basic_operations.delete_customer(1)
        customer = basic_operations.search_customer(1)
        self.assertIsNone(customer)


#if __name__ == '__main__':

#    test = CustomerDBTests()

#     test.create_database()
