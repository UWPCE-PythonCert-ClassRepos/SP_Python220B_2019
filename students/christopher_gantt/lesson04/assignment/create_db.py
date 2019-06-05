'''Creates a database with some data if none exists'''

# pylint Disable=wildcard-import, unused-wildcard-import, broad-except

import logging
from hp_norton_model import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.info('Logger initialized')

CUSTOMER_ID = 0
FIRST_NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
PHONE_NUMBER = 4
EMAIL_ADDRESS = 5
ACTIVITY_STATUS = 6
CREDIT_LIMIT = 7


def fill_empty_database():
    '''fills the empty database with some customers'''
    customers = [('D123', 'Cody', 'Coder', '12345 High St W', 4258291234,
                  'codycoder@gmail.com', True, 10500),
                 ('D456', 'John', 'Smith', None, None,
                  'jsmith@gmail.com', False, None)]

    for customer in customers:
        try:
            with database.transaction():
                new_customer = Customer.create(
                    customer_id=customer[CUSTOMER_ID],
                    first_name=customer[FIRST_NAME],
                    last_name=customer[LAST_NAME],
                    home_address=customer[HOME_ADDRESS],
                    phone_number=customer[PHONE_NUMBER],
                    email_address=customer[EMAIL_ADDRESS],
                    activity_status=customer[ACTIVITY_STATUS],
                    credit_limit=customer[CREDIT_LIMIT])
                new_customer.save()
                LOGGER.info('Customer added to database %s', customer)
        except Exception as exc:
            LOGGER.info('Error creating %s %s', customer[1], customer[2])
            LOGGER.info(exc)


if __name__ == '__main__':
    database.init('customers.db')
    LOGGER.info('customers.db database initialized')

    database.create_tables([Customer])
    LOGGER.info('Customer schema created in database')

    fill_empty_database()

    database.close()
    LOGGER.info('database closed')
