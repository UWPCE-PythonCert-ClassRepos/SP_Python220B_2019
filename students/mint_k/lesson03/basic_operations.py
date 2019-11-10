from customer_model import *

import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Working with Customer class')
LOGGER.info('Note how I use constants and a list of tuples as a simple schema')
LOGGER.info('Normally you probably will have prompted for this from a user')

PERSON_NAME = 0
LIVES_IN_TOWN = 1
NICKNAME = 2

def add_customer(customer_id, name, lastname, home_address, 
                 phone_number, email_address, status, credit_limit):
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                customer_name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                customer_status=status,
                credit_limit=credit_limit)
            new_customer.save()
            LOGGER.info('New customer added to the database')
    except (OperationalError, IntegrityError, DoesNotExist) as myerror:
        LOGGER.info(f'Error occured while adding customer: {customer_id} to database')
        LOGGER.info(myerror)

people = [
    ('Andrew', 'Sumner', 'Andy'),
    ('Peter', 'Seattle', None),
    ('Susan', 'Boston', 'Beannie'),
    ('Pam', 'Coventry', 'PJ'),
    ('Steven', 'Colchester', None),
    ]

DATABASE.close()