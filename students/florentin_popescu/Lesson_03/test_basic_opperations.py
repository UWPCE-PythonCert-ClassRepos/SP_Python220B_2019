# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:57:06 2019
@author: Florentin Popescu
"""
#pylint: disable=W0401  #disable 'Wildcard import peewee'
#pylint: disable=W0614
#pylint: disable=W0703

# imports
import logging
import unittest
from peewee import *

# import external files
import basic_operations
from basic_operations import *
from customer_model import Customer

#======================================
#set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#======================================
# define database
#DATABASE = SqliteDatabase(':memory:')
DATABASE = SqliteDatabase("customers.db")

#======================================
class TestOperations(unittest.TestCase):
    """
        test methods
    """
    #----------------------------------
    def test_add_customer(self):
        """
            test customer addition
        """
        # define a test customer
        inserted_customer = ("1", "Lara", "Croft", "Los Angeles",
                             "private01@yahoo.com", "888-888-8888",
                             "active", 100.00, "01-04-2019",
                             "02-04-2019", "03-04-2019", "tennis")

        # add customer to database via 'add_customer' method
        basic_operations.add_customer(inserted_customer[0],
                                      inserted_customer[1],
                                      inserted_customer[2],
                                      inserted_customer[3],
                                      inserted_customer[4],
                                      inserted_customer[5],
                                      inserted_customer[6],
                                      inserted_customer[7],
                                      inserted_customer[8],
                                      inserted_customer[9],
                                      inserted_customer[10],
                                      inserted_customer[11])

        # retrive customer from database and compare with inserted
        try:
            #open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # retrive customer record by id '1' from database
            db_record = Customer.get_by_id(inserted_customer[0])

            # record all info about retrived customer
            retrived_customer = (db_record.customer_id,
                                 db_record.first_name,
                                 db_record.last_name,
                                 db_record.home_address,
                                 db_record.email_address,
                                 db_record.phone_number,
                                 db_record.status,
                                 db_record.credit_limit,
                                 db_record.join_date,
                                 db_record.insertion_date,
                                 db_record.time_stamp,
                                 db_record.hobby)

            # test if the record retrived is the same as inserted
            self.assertEqual(inserted_customer, retrived_customer)
            LOGGER.info("test of 'add_customer' sucesfull")

        except IndexError as err:
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")

        # clean database -----------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # remove tested customer
            for customer in Customer:
                customer.delete_instance()
            LOGGER.info("tested customer removed; database cleared")

        except IndexError as err:
            LOGGER.info("failed to remove customer; database not cleared")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")
            LOGGER.info("==================================")

    #-------------------------------------- above tests OK
    def test_search_customer(self):
        """
            test search method
        """
        # define a test customer
        inserted_customer = ("1", "Lara", "Croft", "Los Angeles",
                             "private01@yahoo.com", "888-888-8888",
                             "active", 100.00, "01-04-2019",
                             "02-04-2019", "03-04-2019", "tennis")

        # add customer to database via 'add_customer' method
        basic_operations.add_customer(inserted_customer[0],
                                      inserted_customer[1],
                                      inserted_customer[2],
                                      inserted_customer[3],
                                      inserted_customer[4],
                                      inserted_customer[5],
                                      inserted_customer[6],
                                      inserted_customer[7],
                                      inserted_customer[8],
                                      inserted_customer[9],
                                      inserted_customer[10],
                                      inserted_customer[11])

        # search customer in database and test if it's the same as inserted
        try:
            # search for customer in database via 'search_customer' method
            searched_customer = basic_operations.search_customer(inserted_customer[0])
            expected_customer = {"customer_id": "1",
                                 "first_name": "Lara",
                                 "last_name": "Croft",
                                 "home_address": "Los Angeles",
                                 "email_address": "private01@yahoo.com",
                                 "phone_number": "888-888-8888",
                                 "status": "active",
                                 "credit_limit": 100.00,
                                 "join_date": "01-04-2019",
                                 "insertion_date": "02-04-2019",
                                 "time_stamp": "03-04-2019",
                                 "hobby": "tennis"}

            # test if customer searched is the same as inserted
            self.assertEqual(searched_customer, expected_customer)
            LOGGER.info("test of 'search_customer' sucesfull")

        except IndexError as err:
            LOGGER.info('searched customer not found')
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")

        # clean database -------------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # remove tested customer
            for customer in Customer:
                customer.delete_instance()
            LOGGER.info("tested customer removed; database cleared")

        except IndexError as err:
            LOGGER.info("failed to remove customer; database not cleared")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")
            LOGGER.info("==================================")

    #-------------------------------------- OK
    def test_delete_customer(self):
        """
            test delete customer method
        """
        # define a test customer
        inserted_customer = ("1", "Lara", "Croft", "Los Angeles",
                             "private01@yahoo.com", "888-888-8888",
                             "active", 100.00, "01-04-2019",
                             "02-04-2019", "03-04-2019", "tennis")

        # add customer to database via 'add_customer' method
        basic_operations.add_customer(inserted_customer[0],
                                      inserted_customer[1],
                                      inserted_customer[2],
                                      inserted_customer[3],
                                      inserted_customer[4],
                                      inserted_customer[5],
                                      inserted_customer[6],
                                      inserted_customer[7],
                                      inserted_customer[8],
                                      inserted_customer[9],
                                      inserted_customer[10],
                                      inserted_customer[11])

        searched_customer = basic_operations.search_customer(inserted_customer[0])
        expected_customer = {"customer_id": "1",
                             "first_name": "Lara",
                             "last_name": "Croft",
                             "home_address": "Los Angeles",
                             "email_address": "private01@yahoo.com",
                             "phone_number": "888-888-8888",
                             "status": "active",
                             "credit_limit": 100.00,
                             "join_date": "01-04-2019",
                             "insertion_date": "02-04-2019",
                             "time_stamp": "03-04-2019",
                             "hobby": "tennis"}

        # test if insertion was succesfull
        self.assertEqual(searched_customer, expected_customer)
        LOGGER.info("customer sucesfully inserted into database")

        # delete inserted customer from database
        try:
            # delete customer using 'delete_customer' method
            basic_operations.delete_customer(inserted_customer[0])
            LOGGER.info("delete operation implemented")

        except (OperationalError, IndexError) as err:
            LOGGER.info("customer not deleted")
            LOGGER.info(err)

        # test deletion -----------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # search inserted customer
            try:
                basic_operations.search_customer(inserted_customer[0])

            except Exception:
                LOGGER.info("searched customer not found in database")
                LOGGER.info("test of 'delete_customer' succesfull")

        except OperationalError as err:
            LOGGER.info("connection to database failed")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")

        # clean database --------------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # remove inserted customer
            for customer in Customer:
                customer.delete_instance()
            LOGGER.info("database cleared")

        except IndexError as err:
            LOGGER.info("failed to remove customer; database not cleared")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")
            LOGGER.info("==================================")

    #--------------------------------------
    def test_update_credit(self):
        """
            test credit update method
        """
        # define a test customer
        inserted_customer = ("1", "Lara", "Croft", "Los Angeles",
                             "private01@yahoo.com", "888-888-8888",
                             "active", 100.00, "01-04-2019",
                             "02-04-2019", "03-04-2019", "tennis")

        # add customer to database via 'add_customer' method
        basic_operations.add_customer(inserted_customer[0],
                                      inserted_customer[1],
                                      inserted_customer[2],
                                      inserted_customer[3],
                                      inserted_customer[4],
                                      inserted_customer[5],
                                      inserted_customer[6],
                                      inserted_customer[7],
                                      inserted_customer[8],
                                      inserted_customer[9],
                                      inserted_customer[10],
                                      inserted_customer[11])

        # update credit limit for inserted customer
        try:
            # set customer's new credit limit to $200 via 'update_credit'
            basic_operations.update_credit(inserted_customer[0], 200)

            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")
            # retrive customer with updated credit
            updated_credit_customer = Customer.get_by_id(inserted_customer[0])

            # get credit limit of updated customer
            credit_update = updated_credit_customer.credit_limit

            # test if the customer credit has been indeed rised to $200
            self.assertEqual(credit_update, 200)
            LOGGER.info("credit limit updated sucesfully")

        except IndexError as err:
            LOGGER.info("credit limit not updated")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")

        # clean database --------------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # remove inserted customer
            for customer in Customer:
                customer.delete_instance()
            LOGGER.info("inserted customer removed; database cleared")

        except IndexError as err:
            LOGGER.info("failed to remove customer; database not cleared")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")
            LOGGER.info("==================================")

    #--------------------------------------
    def test_update_status(self):
        """
            test update status
        """
        # define a test customer
        inserted_customer = ("1", "Lara", "Croft", "Los Angeles",
                             "private01@yahoo.com", "888-888-8888",
                             "active", 100.00, "01-04-2019",
                             "02-04-2019", "03-04-2019", "tennis")

        # add customer to database via 'add_customer' method
        basic_operations.add_customer(inserted_customer[0],
                                      inserted_customer[1],
                                      inserted_customer[2],
                                      inserted_customer[3],
                                      inserted_customer[4],
                                      inserted_customer[5],
                                      inserted_customer[6],
                                      inserted_customer[7],
                                      inserted_customer[8],
                                      inserted_customer[9],
                                      inserted_customer[10],
                                      inserted_customer[11])

        # update inserted customer's status
        try:
            # update inserted customer's status via 'update_status' method
            basic_operations.update_status(inserted_customer[0], "inactive")

            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # retrive inserted customer from database
            updated_status_customer = Customer.get_by_id(inserted_customer[0])

            # get the new status of customer
            new_status = updated_status_customer.status

            # test if the status has indeed changed
            self.assertEqual(new_status, "inactive")
            LOGGER.info("status changed succesfully")

        except IndexError as err:
            LOGGER.info("status not updated")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")

       # clean database -------------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # remove inserted customer
            for customer in Customer:
                customer.delete_instance()
            LOGGER.info("inserted customer removed; database cleared")

        except IndexError as err:
            LOGGER.info("failed to remove customer; database not cleared")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")
            LOGGER.info("==================================")

    #--------------------------------------
    def test_list_active_customers(self):
        """
            test active customers
        """
        # define a test customer
        inserted_customer = ("1", "Lara", "Croft", "Los Angeles",
                             "private01@yahoo.com", "888-888-8888",
                             "active", 100.00, "01-04-2019",
                             "02-04-2019", "03-04-2019", "tennis")

        # add customer to database via 'add_customer' method
        basic_operations.add_customer(inserted_customer[0],
                                      inserted_customer[1],
                                      inserted_customer[2],
                                      inserted_customer[3],
                                      inserted_customer[4],
                                      inserted_customer[5],
                                      inserted_customer[6],
                                      inserted_customer[7],
                                      inserted_customer[8],
                                      inserted_customer[9],
                                      inserted_customer[10],
                                      inserted_customer[11])

        # test the  list of active customers
        try:
            # retrive the a list of active customers from database
            number_list_active = basic_operations.list_active_customers()

            # test if inserted active customer exists in database
            self.assertEqual(list(number_list_active.keys())[0], 1)
            LOGGER.info("number of customers in database tested sucesfully")

            # test if inserted customer is in list of active customers
            self.assertEqual(list(number_list_active.values())[0], [inserted_customer[0]])
            LOGGER.info("id %s customer exist in database", inserted_customer[0])

        except (IndexError, #AssertionError,
                IntegrityError, OperationalError) as err:
            LOGGER.info(err)

        # clean database -------------------
        try:
            # open database
            DATABASE.connect()
            DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

            # remove inserted customer
            for customer in Customer:
                customer.delete_instance()
            LOGGER.info("inserted customer removed; database cleared")

        except IndexError as err:
            LOGGER.info("failed to remove customer; database not cleared")
            LOGGER.info(err)

        finally:
            # close database
            DATABASE.close()
            LOGGER.info("database closed")
            LOGGER.info("==================================")

#===========================================
if __name__ == '__main__':
    unittest.main()
#===========================================
