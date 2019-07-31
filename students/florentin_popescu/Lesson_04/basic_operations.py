# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:03:35 2019
@author: Florentin Popescu
"""
# pylint: disable-msg=too-many-arguments
# pylint: disable=W0401  #disable 'Wildcard import peewee'
# pylint: disable=W0614

# imports
import logging
from peewee import *

# import external files
from customer_model import *
from customer_model import Customer
# ========================================
# set basic looging level as INFO
#logging.basicConfig(level=logging.INFO)
#LOGGER = logging.getLogger(__name__)

LOG_FORMATTER = logging.Formatter("%(asctime)s %(filename)s:%(lineno)-4d \
                                  %(levelname)s %(message)s")
FILE_HANDLER = logging.FileHandler('logs.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(LOG_FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

LOGGER.info("basic_operation.py")

# ========================================
# define database
DATABASE = SqliteDatabase("customers.db")
LOGGER.info("database 'customers.db' initialised")

# ========================================


def add_customer(customer_id, first_name, last_name,
                 home_address, email_address, phone_number,
                 status, credit_limit, join_date,
                 insertion_date, time_stamp, hobby):
    """
        add customer info to database
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # insert customers to database
        with DATABASE.transaction():
            new_customer = Customer.create(customer_id=customer_id,
                                           first_name=first_name,
                                           last_name=last_name,
                                           home_address=home_address,
                                           email_address=email_address,
                                           phone_number=phone_number,
                                           status=status,
                                           credit_limit=credit_limit,
                                           join_date=join_date,
                                           insertion_date=insertion_date,
                                           time_stamp=time_stamp,
                                           hobby=hobby)
            new_customer.save()
            LOGGER.info("new customer added to database")

    except IntegrityError as err:
        LOGGER.error("error creating a non-unique customer id %s", customer_id)
        LOGGER.error(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")
# ========================================


def search_customer(customer_id):
    """
        search a customer by id
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # search a customer by id
        searched_customer = Customer.get_by_id(customer_id)
        LOGGER.info("customer %s found", customer_id)

        # retrive full info for searched customer from database
        return {"customer_id": searched_customer.customer_id,
                "first_name": searched_customer.first_name,
                "last_name": searched_customer.last_name,
                "home_address": searched_customer.home_address,
                "email_address": searched_customer.email_address,
                "phone_number": searched_customer.phone_number,
                "status": searched_customer.status,
                "credit_limit": searched_customer.credit_limit,
                "join_date": searched_customer.join_date,
                "insertion_date": searched_customer.insertion_date,
                "time_stamp": searched_customer.time_stamp,
                "hobby": searched_customer.hobby}

    except DoesNotExist as err:
        LOGGER.info("customer id %s not found", customer_id)
        LOGGER.info(err)
        return {}

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")
# ========================================


def delete_customer(customer_id):
    """
        delete a customer by id
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # remove customer by id
        Customer.get_by_id(customer_id).delete_instance()
        LOGGER.info("id %s customer deleted", customer_id)

    except DoesNotExist as err:
        LOGGER.info("customer with id %s not deleted", customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")
# ========================================


def update_credit(customer_id, credit_limit):
    """
        search customer by id and update credit limit
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # retrive customer by id
        searched_customer = Customer.get_by_id(customer_id)

        # update customer's credit limit
        searched_customer.credit_limit = credit_limit
        LOGGER.info("credit limit updated for customer id %s", customer_id)

        # save updated customer
        searched_customer.save()

    except DoesNotExist as err:
        LOGGER.info("customer id %s not found", customer_id)
        LOGGER.info("credit limit of %s for customer id %s not updated",
                    credit_limit, customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")
# ========================================


def update_status(customer_id, new_status):
    """
        update customer status
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # search customer by id
        searched_customer = Customer.get_by_id(customer_id)
        # check searched customer's status and update it if active or inactive
        if new_status in ("active", "inactive"):
            searched_customer.status = new_status
            LOGGER.info("status updated for customer id %s", customer_id)
            # save updated customer
            searched_customer.save()
        else:
            LOGGER.info("status neither active or inactive")
            LOGGER.info("status wasn't updated")

    except DoesNotExist as err:
        LOGGER.info("customer id %s not found", customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")
# ========================================


def list_active_customers():
    """
        use list comprehension
        to return number of active customers and their ids
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # return number of active customers and their ids
        active_ids = [cid.customer_id for cid in
                      Customer.select().where(Customer.status == "active")
                      if Customer.customer_id is not None]
        LOGGER.info("database has %s active customers", len(active_ids))

        if not bool(len(active_ids)):
            raise ValueError('empty database')

        return {len(active_ids): active_ids}

    except ValueError as err:
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")
# ========================================


def display_customers():
    """
        use generator and list comprehension
        to display customer info
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        LOGGER.info("Display the customer name")
        info = [name for name in
                ((f"{customer.first_name}" + " "
                  + f"{customer.last_name}") for customer in Customer)]

        if not bool(len(info)):
            raise ValueError('EmptyDatabase')

        return info

    except ValueError as err:
        LOGGER.info("customer name cannot be displayed \
                    because there are no customers in database")
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

# ========================================
# --------------- END --------------------
# ========================================
