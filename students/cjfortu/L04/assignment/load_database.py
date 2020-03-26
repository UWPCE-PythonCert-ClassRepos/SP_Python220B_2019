#!/usr/bin/env python
"""
Load the customer database.
"""

from customer_model import *
from customer_data_raw import customers


def add_customers():
    """
    Build the database from the raw data.
    """
    LOGGER.info('Establishing database')

    try:
        for customer in customers:
            with database.transaction():
                new_customer = Customer.create(
                    customer_id=customer[0],
                    name=customer[1],
                    last_name=customer[2],
                    home_address=customer[3],
                    phone_number=customer[4],
                    email_address=customer[5],
                    status=customer[6],
                    credit_limit=customer[7])
                new_customer.save()
                LOGGER.info(f'Database add successful {customer[0]}')

    except Exception as exc:
        LOGGER.info(f'Error creating = {customer[0]}')
        LOGGER.info(exc)

    finally:
        LOGGER.info('database closes')
        database.close()


if __name__ == '__main__':
    database.connect()
    database.execute_sql('PRAGMA foreign_keys = ON;')
    database.drop_tables([Customer])
    database.create_tables([Customer])
    add_customers()
