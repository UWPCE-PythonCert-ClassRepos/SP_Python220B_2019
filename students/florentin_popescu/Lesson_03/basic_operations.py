# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:54:36 2019
@author: Florentin Popescu
"""
#pylint: disable-msg=too-many-arguments
#pylint: disable=W0401  #disable 'Wildcard import peewee'
#pylint: disable=W0614

# imports
import logging
from peewee import *

# import external files
from customer_model import Customer

#========================================
#set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

#========================================
# define database
DATABASE = SqliteDatabase("customers.db")

#========================================
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
            # message if customer added
            LOGGER.info("new customer added to database")

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except (InternalError, InterfaceError, IntegrityError) as err:
        LOGGER.info("error creating a non-unique customer id %s", customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

#======================================== OK
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
                #-------------------------
                "join_date": searched_customer.join_date,
                "insertion_date": searched_customer.insertion_date,
                "time_stamp": searched_customer.time_stamp,
                "hobby": searched_customer.hobby}

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except IntegrityError as err:
        LOGGER.info("customer not found")

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

#======================================== OK
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

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except IntegrityError as err:
        LOGGER.info("customer with id %s not found", customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

#======================================== ???
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

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except (IntegrityError, DataError) as err:
        LOGGER.info("customer id %s not found", customer_id)
        LOGGER.info("credit limit of %s for customer id %s not updated",
                    credit_limit, customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

#========================================
def update_status(customer_id, new_status):
    """
        update customer status
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # seatch customer by id
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

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except IntegrityError as err:
        LOGGER.info("customer id %s not found", customer_id)
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

#========================================
def list_active_customers():
    """
        return number of active customers and list their ids
    """
    try:
        # open database
        DATABASE.connect()
        DATABASE.execute_sql('PRAGMA foreign_keys=ON;')
        LOGGER.info("connected to database")

        # return number of active customers and their ids
        active_ids = [cid.customer_id for cid in
                      Customer.select().where(Customer.status == "active")]
        LOGGER.info("database has %s active customers", len(active_ids))
        return {len(active_ids): active_ids}

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except (IntegrityError, DataError) as err:
        LOGGER.info(err)

    finally:
        # close database
        DATABASE.close()
        LOGGER.info("database closed")

#========================================
#--------------- END --------------------
#========================================
