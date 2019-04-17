"""Creates a full suite of tests for basic_operations.py"""

import logging
import unittest
import sys
sys.path.append('C:/Users/allth/OneDrive/Desktop/Python/Python220/SP_Python220B_2019/'
                'students/dfspray/Lesson04/src')
from peewee import *
import src
from src import basic_operations
from src import customer_model_schema
from src.customer_model_schema import Customers

DATABASE = SqliteDatabase('customers.db')
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class TestOperations(unittest.TestCase):
    """Tests the methods of basic_operations"""
    def test_add_customer(self):
        """This method tests that 3 customers are successfully added to the database"""
        basic_operations.add_customer(None, None, None, None, None, None, None, None)
        basic_operations.add_customer('001', 'Joey', 'Smith', '123 Jackson Street', 1234567890,
                                      'joey@gmail.com', 'active', 1000.00)
        basic_operations.add_customer('002', 'Alex', 'Peterson', '123 Jefferson Street', 2345678901,
                                      'alex@gmail.com', 'active', 1000.00)
        basic_operations.add_customer('003', 'Aaron', 'Dickson', '123 Rainier Street', 3456789012,
                                      'aaron@gmail.com', 'inactive', 1000.00)
        basic_operations.add_customer('003', 'Aaron', 'Dickson', '123 Rainier Street', 3456789012,
                                      'aaron@gmail.com', 'active', 1000.00)


        try:
            DATABASE.connect()
            DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

            added_customer1 = Customers.get(Customers.customer_id == '001')
            actual_customer1 = (added_customer1.customer_id, added_customer1.name,
                                added_customer1.lastname, added_customer1.home_address,
                                added_customer1.phone_number, added_customer1.email_address,
                                added_customer1.status, added_customer1.credit_limit)

            added_customer2 = Customers.get(Customers.customer_id == '002')
            actual_customer2 = (added_customer2.customer_id, added_customer2.name,
                                added_customer2.lastname, added_customer2.home_address,
                                added_customer2.phone_number, added_customer2.email_address,
                                added_customer2.status, added_customer2.credit_limit)

            added_customer3 = Customers.get(Customers.customer_id == '003')
            actual_customer3 = (added_customer3.customer_id, added_customer3.name,
                                added_customer3.lastname, added_customer3.home_address,
                                added_customer3.phone_number, added_customer3.email_address,
                                added_customer3.status, added_customer3.credit_limit)

        except Exception as ex:
            LOGGER.info(ex)

        finally:
            LOGGER.info('Closing database')
            DATABASE.close()

        expected_customer1 = ('001', 'Joey', 'Smith', '123 Jackson Street', '1234567890',
                              'joey@gmail.com', 'active', 1000.00)
        expected_customer2 = ('002', 'Alex', 'Peterson', '123 Jefferson Street', '2345678901',
                              'alex@gmail.com', 'active', 1000.00)
        expected_customer3 = ('003', 'Aaron', 'Dickson', '123 Rainier Street', '3456789012',
                              'aaron@gmail.com', 'inactive', 1000.00)

        self.assertEqual(actual_customer1, expected_customer1)
        self.assertEqual(actual_customer2, expected_customer2)
        self.assertEqual(actual_customer3, expected_customer3)

        try:
            DATABASE.connect()
            DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
            added_customer1.delete_instance()
            added_customer2.delete_instance()
            added_customer3.delete_instance()
            LOGGER.info('Successfully deleted customers')

        except Exception as ex:
            LOGGER.info('Could not delete customer')
            LOGGER.info(ex)

        finally:
            LOGGER.info('Closing database')
            DATABASE.close()

    def test_search_customer(self):
        """This method tests that the customer search function works properly"""
        add_test_customer()
        LOGGER.info('Closing database')
        DATABASE.close()
        actual_searched_customer1 = basic_operations.search_customer('001')
        actual_searched_customer2 = basic_operations.search_customer('002')
        expected_searched_customer1 = {'customer_id': '001',
                                       'name': 'Joey', 'lastname': 'Smith',
                                       'home_address': '123 Jackson Street',
                                       'phone_number': '1234567890',
                                       'email_address': 'joey@gmail.com',
                                       'status': 'active', 'credit_limit': 1000.00}
        expected_searched_customer2 = {}

        self.assertEqual(actual_searched_customer1, expected_searched_customer1)
        self.assertEqual(actual_searched_customer2, expected_searched_customer2)

        delete_test_customer()

    def test_update_credit(self):
        """Test that you can update a customer's credit limit"""

        add_test_customer()
        LOGGER.info('Closing database')
        DATABASE.close()

        basic_operations.update_customer_credit('002', 2000)
        updated_credit_customer1 = Customers.get(Customers.customer_id == '001')
        actual_credit_update1 = updated_credit_customer1.credit_limit
        expected_credit_update1 = 1000.00

        self.assertEqual(actual_credit_update1, expected_credit_update1)

        basic_operations.update_customer_credit('001', 2000)
        updated_credit_customer2 = Customers.get(Customers.customer_id == '001')
        actual_credit_update2 = updated_credit_customer2.credit_limit
        expected_credit_update2 = 2000.00

        self.assertEqual(actual_credit_update2, expected_credit_update2)

        delete_test_customer()

    def test_list_active(self):
        """Test that you can display the correct number of active customers"""

        actual_customer_count1 = basic_operations.list_active_customers()
        self.assertEqual(actual_customer_count1, 0)

        add_test_customer()
        LOGGER.info('Closing database')
        DATABASE.close()

        actual_customer_count2 = basic_operations.list_active_customers()
        self.assertEqual(actual_customer_count2, 1)

        delete_test_customer()

    def test_delete_customer(self):
        """Test that you can delete a customer"""

        add_test_customer()

        added_customer = Customers.get(Customers.customer_id == '001')
        actual_customer = (added_customer.customer_id, added_customer.name,
                           added_customer.lastname, added_customer.home_address,
                           added_customer.phone_number, added_customer.email_address,
                           added_customer.status, added_customer.credit_limit)
        expected_customer = ('001', 'Joey', 'Smith', '123 Jackson Street', '1234567890',
                             'joey@gmail.com', 'active', 1000.00)
        basic_operations.delete_customer('0001')

        self.assertEqual(actual_customer, expected_customer)

        LOGGER.info('Closing database')
        DATABASE.close()

        basic_operations.delete_customer('001')

        try:
            DATABASE.connect()
            DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
            LOGGER.info('Successfully connected to the database')
            searched_customer = Customers.get(Customers.customer_id == '001')
            LOGGER.info('Customer Found!')
            deleted_customer = {'customer_id': searched_customer.customer_id,
                                'name': searched_customer.name,
                                'lastname': searched_customer.lastname,
                                'home_address': searched_customer.home_address,
                                'phone_number': searched_customer.phone_number,
                                'email_address': searched_customer.email_address,
                                'status': searched_customer.status,
                                'credit_limit': searched_customer.credit_limit}

        except Exception as ex:
            LOGGER.info('Error finding customer 001')
            LOGGER.info(ex)
            deleted_customer = {}

        self.assertEqual(deleted_customer, {})
        LOGGER.info('Closing database')
        DATABASE.close()

    def test_update_status(self):
        """Test that you can update a customer's status to only either active or inactive"""
        add_test_customer()
        LOGGER.info('Closing database')
        DATABASE.close()

        basic_operations.update_status('001', 2000)
        updated_status_customer_fail = Customers.get(Customers.customer_id == '001')
        actual_status_update_fail = updated_status_customer_fail.status
        expected_status_fail = 'active'

        self.assertEqual(actual_status_update_fail, expected_status_fail)

        basic_operations.update_status('002', 'inactive')
        updated_status_customer_fail2 = Customers.get(Customers.customer_id == '001')
        actual_status_update_fail2 = updated_status_customer_fail2.status
        expected_status_fail2 = 'active'

        self.assertEqual(actual_status_update_fail2, expected_status_fail2)

        self.assertEqual(actual_status_update_fail, expected_status_fail)
        basic_operations.update_status('001', 'inactive')
        updated_status_customer_success = Customers.get(Customers.customer_id == '001')
        actual_status_update_success = updated_status_customer_success.status
        expected_status_success = 'inactive'

        self.assertEqual(actual_status_update_success, expected_status_success)

        basic_operations.update_status('001', 'active')
        updated_status_customer_active = Customers.get(Customers.customer_id == '001')
        actual_status_update_active = updated_status_customer_active.status
        expected_status_active = 'active'

        self.assertEqual(actual_status_update_active, expected_status_active)

        delete_test_customer()

def add_test_customer():
    """This method adds a single test customer, and leaves the database open"""

    try:
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys = ON;')
        LOGGER.info('Successfully connected to the database')
        with DATABASE.transaction():
            new_customer = Customers.create(customer_id='001',
                                            name='Joey',
                                            lastname='Smith',
                                            home_address='123 Jackson Street',
                                            phone_number='1234567890',
                                            email_address='joey@gmail.com',
                                            status='active',
                                            credit_limit=float(1000.00))
        new_customer.save()
        LOGGER.info('Successfully added new customer')

    except Exception as ex:
        LOGGER.info('Error creating 001')
        LOGGER.info(ex)

def delete_test_customer():
    """This method deletes the test customer, Joey, then closes the database"""

    try:
        delete_customer = Customers.get(Customers.customer_id == '001')
        delete_customer.delete_instance()
        LOGGER.info('Successfully deleted customer 001')

    except Exception as ex:
        LOGGER.info('Error finding customer 001')
        LOGGER.info('Customer was not deleted')
        LOGGER.info(ex)

    finally:
        LOGGER.info('Closing database')
        DATABASE.close()

if __name__ == '__main__':
    unittest.main()
