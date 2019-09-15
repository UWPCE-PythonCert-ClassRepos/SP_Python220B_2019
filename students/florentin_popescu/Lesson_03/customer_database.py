# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 09:56:03 2019
@author: Florentin Popescu
"""
# pylint: disable=W0401  #disable 'Wildcard import peewee'
# pylint: disable=W0614

# imports
import logging
from peewee import *

# import external files
from customer_model import Customer

# ========================================
# set basic looging level as INFO
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# ========================================
# define database
DATABASE = SqliteDatabase("customers.db")

# open database
DATABASE.connect()
DATABASE.execute_sql("PRAGMA foreign_keys = ON;")

# ========================================
# initialize database
DATABASE.create_tables([Customer])
DATABASE.close()

# ========================================
# sample customers for insertion to database
CUSTOMERS = [
        ("1", "Florentin", "Popescu", "Chicago", "private01@yahoo.com",
         "312-312-1234", "active", 100.00, "01-01-2019", "02-01-2019",
         "01-01-2019", "football_1"),
        ("2", "Florentino", "Popesco", "Chicago", "private02@yahoo.com",
         "312-312-2345", "inactive", 200.00, "01-02-2019", "02-02-2019",
         "01-02-2019", "football_2"),
        ("3", "Florentinoo", "Popescoo", "Chicago", "private03@yahoo.com",
         "312-312-3456", "active", 300.00, "01-03-2019", "02-03-2019",
         "01-02-2019", "football_3")
        ]

# insert sample customers to database
for customer in CUSTOMERS:
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer[0],
                first_name=customer[1],
                last_name=customer[2],
                home_address=customer[3],
                email_address=customer[4],
                phone_number=customer[5],
                status=customer[6],
                credit_limit=customer[7],
                join_date=customer[8],
                insertion_date=customer[9],
                time_stamp=customer[10],
                hobby=customer[11])
            new_customer.save()

    except OperationalError as err:
        LOGGER.info("conection to database failed")
        LOGGER.info(err)

    except (IntegrityError, InternalError, InterfaceError) as err:
        LOGGER.info("Error creating a non-unique customer id %s", customer[0])
        LOGGER.info(err)

# after sample insertion display customers added to database
for customer in Customer:
    LOGGER.info(customer.__str__)
    LOGGER.info("customer: %s- %s, %s",
                customer.customer_id,
                customer.last_name,
                customer.first_name)

# clean database by removing sample customers
for customer in Customer:
    LOGGER.info("customer id %s erased from database", customer.customer_id)
    customer.delete_instance()

# close database
DATABASE.close()
LOGGER.info("database closed")
