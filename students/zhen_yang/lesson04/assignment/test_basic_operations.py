""" This module test the functions written in basic_operations.py """
from unittest import TestCase
import code_dr.basic_operations as bo
from code_dr.customer_model import Customer, database


class basic_operationsTests(TestCase):
    """ This class defines unit test fuctions for basic_operations.py """

    def test_add_customer(self):
        """ This function defines unit test fuction for add_customer() """
        # create an empty database for testing
        database.drop_tables([Customer])
        database.create_tables([Customer])

        bo.logger.info('-- Testing adding new customer --')
        arg_list = [[1, 'Emily', 'Yang', '121 Main street NewYork',
                     2062847320, 'yange@hotmail.com', True, 10000],
                    [2, 'Adam', 'Chilly', '233 Jone street LA', '4342941868',
                     'chillya@hotmail.com', True, 5000],
                    [3, 'Steve', 'Wagon', '4508 Lord Ave Seattle', '6879337640',
                     'wagons@gmail.com', False, 0],
                    [4, 'Jone', 'Comba', '1129 Brand street Boise',
                     '3745689770', 'combaj@gmail.com', False, 100],
                    [5, 'Zaler', 'Danny', '29 Colb street Portland',
                     '2323456787', 'dannyz@yahoo.com', True, 1000]
                    ]

        for i in range(5):
            bo.add_customer(*arg_list[i])

        customer = Customer.get(Customer.customer_id == 1)
        self.assertEqual(customer.name, 'Emily')
        self.assertEqual(customer.lastname, 'Yang')
        self.assertEqual(customer.home_address, '121 Main street NewYork')
        self.assertEqual(customer.phone_number, '2062847320')
        self.assertEqual(customer.email_address, 'yange@hotmail.com')
        self.assertEqual(customer.status, True)
        self.assertEqual(customer.credit_limit, 10000)
        self.assertEqual(len(Customer), 5)

        for customer in Customer:
            bo.logger.info(f'{customer.name} {customer.home_address} '
                           f'{customer.phone_number} {customer.email_address} '
                           f'{customer.status} {customer.credit_limit}')
        bo.logger.info('-- End of Testing adding new customer --\n')

    def test_search_customer(self):
        """ This function defines unit test fuction for search_customer() """
        bo.logger.info('-- Testing search an existing customer.--')
        # test seraching the exitsting customer
        the_customer = bo.search_customer(2)
        key_list = ['name', 'lastname', 'phone_number', 'email_address']
        val_list = ['Adam', 'Chilly', '4342941868', 'chillya@hotmail.com']
        expect_res = dict(zip(key_list, val_list))
        self.assertEqual(the_customer, expect_res)

        # test seraching the non-exitsting customer
        bo.logger.info('-- Testing search a non-existing customer.--')
        the_customer = bo.search_customer(12)
        expect_res = {}
        self.assertEqual(the_customer, expect_res)
        bo.logger.info('-- End of Testing searching customer --\n')

    def test_delete_customer(self):
        """ This function defines unit test fuction for delete_customer() """
        bo.logger.info('-- Testing delete an existing customer. --')
        bo.delete_customer(5)
        the_customer = bo.search_customer(5)
        expect_res = {}
        self.assertEqual(the_customer, expect_res)
        bo.logger.info('-- Testing delete non-existing customer. --')
        bo.delete_customer(5)
        bo.logger.info('-- End of Testing deleteing customer --\n')

    def test_update_customer_credit(self):
        """
            This function defines unit test fuction for update_customer_credit()
        """
        bo.logger.info('-- Testing update existing customer credit limit.--')

        # test existing customer
        bo.update_customer_credit(3, 300)
        self.assertEqual(Customer.get(Customer.customer_id == 3).credit_limit,
                         300)
        # test non existing customer
        bo.logger.info('-- Testing update non-existing customer credit'
                       'limit.--')
        bo.update_customer_credit(800, 300)
        bo.logger.info('-- End of Testing updating customer --\n')

    def test_list_active_customers(self):
        """
            This function defines unit test fuction for list_active_customers()
        """
        bo.logger.info('-- Testing the number of active customers.--')
        num = bo.list_active_customers()
        bo.logger.info(f'-- The number of active customers: {num} --\n')
        self.assertEqual(num, 2)
        bo.logger.info('-- End of Testing num of active customers --\n')
