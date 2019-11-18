"""
Create customer.db and add data
"""
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import

import logging
from peewee import *
from customer_model import Model, BaseModel, Customer, database


CUSTOMER_ID = 0
CUSTOMER_NAME = 1
CUSTOMER_LAST_NAME = 2
CUSTOMER_ADDRESS = 3
CUSTOMER_PHONE_NUMBER = 4
CUSTOMER_EMAIL = 5
CUSTOMER_STATUS = 6
CUSTOMER_CREDIT_STATUS = 7

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info("Started logger")



def open_database():
    """Open the database to create tables"""

    #BaseModel.Meta.database = database
    logging.info('create table')
    database.create_tables([Customer])

# def add_customers():
#     logging.info('create table')
#     database.create_tables([Customer])

    # customer = [('D421', 'Susie', 'Smith', '2424 No Name Rd', '4256789255',
    #              'susies@yahoo.com', True, 9000.00),
    #             ('D845', 'Mac', 'Lee', '12 Street', '6254779825',
    #              'macaroni@comcast.com', False, 200.00 )]

    # for customer in customer:
    #     try:
    #         with database.transaction():
    #             new_customer = Customer.create(
    #             customer_id = customer[CUSTOMER_ID],
    #             customer_name = customer[CUSTOMER_NAME],
    #             customer_last_name = customer[CUSTOMER_LAST_NAME],
    #             customer_address = customer[CUSTOMER_ADDRESS],
    #             customer_phone_number = customer[CUSTOMER_PHONE_NUMBER],
    #             customer_email = customer[CUSTOMER_EMAIL],
    #             customer_status = customer[CUSTOMER_STATUS],
    #             customer_credit_status = customer[CUSTOMER_CREDIT_STATUS])
    #             LOGGER.info("created %d rows", new_customer.save())

    #     except Exception as e:
    #         LOGGER.info(f"Error adding = {customer[CUSTOMER_ID]}")
    #         LOGGER.info(e)

    # LOGGER.info('Data added')


if __name__ == "__main__":
    open_database()
    #add_customers()
    LOGGER.info('closing db')
    database.close()
