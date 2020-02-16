import logging
from peewee import *
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Customer class')

CUST_ID = 0
NAME = 1
LAST_NAME = 2
HOME_ADDRESS = 3
EMAIL_ADDRESS = 4
PHONE = 5
STATUS = 6
CREDIT_LIMIT = 7

customers = [
    ('A500', 'Andrew', 'Smith',
     '23 Railroad Street Matthews, NC 28104', 'andrew@hpnorton.com',
     '202-555-0134', True, 1000),
    ('A501', 'David', 'Nelson',
     '7 Blackburn Drive Tualatin, OR 97062', 'david@hpnorton.com',
     '202-555-0169', True, 0),
    ('B200', 'Kate', 'Harris',
     '638 Cactus St. Wilmington, MA 01887', 'kate@hpnorton.com',
     '202-555-0169', False, 1000)
    ]


def add_customer(customer_id, name, last_name,
                 home_address, email_address,
                 phone_number, status, credit_limit):
    ''' add new customers to the database '''
    customer = (customer_id, name, last_name,
                home_address, email_address,
                phone_number, status, credit_limit)
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id = customer[CUST_ID],
                name = customer[NAME],
                last_name = customer[LAST_NAME],
                home_address = customer[HOME_ADDRESS],
                email_address = customer[EMAIL_ADDRESS],
                phone_number = customer[PHONE],
                status = customer[STATUS],
                credit_limit = customer[CREDIT_LIMIT])
            new_customer.save()
            logger.info(f'{name} {last_name} added to database')
    except Exception as e:
        logger.info(f'Error creating customer id {customer_id}')
        logger.info(e)

def search_customer(customer_id):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        
    except DoesNotExist:
        raise ValueError(f'{customer.customer_id} not found in database')

    return {'name': customer.name, 
            'last_name': customer.last_name,
            'email_address': customer.email_address, 
            'phone_number': customer.phone_number}

def delete_customer(customer_id):
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
        logger.info(f'{customer.name} has been deleted')

    except DoesNotExist:
        raise ValueError(f'{customer.customer_id} not found in database')

def update_customer_credit(customer_id, credit_limit):
    ''' update customers credit limit '''
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.credit_limit = credit_limit
        customer.save()
        logger.info(f'{customer.credit_limit}')

    except DoesNotExist:
        raise ValueError(f'{customer.customer_id} not found in database')

def list_active_customers():
    try:
        active_customers = Customer.select().where(Customer.status).count()
        active_cust_name = Customer.select().where(Customer.status)

        logger.info(f'active customer count is {active_customers}')
    except:
        pass
    return active_customers
# add_customer(customers[0][CUST_ID], customers[0][NAME], customers[0][LAST_NAME],
#              customers[0][HOME_ADDRESS], customers[0][EMAIL_ADDRESS],
#              customers[0][PHONE], customers[0][STATUS], customers[0][CREDIT_LIMIT])

# add_customer(customers[1][CUST_ID], customers[1][NAME], customers[1][LAST_NAME],
#              customers[1][HOME_ADDRESS], customers[1][EMAIL_ADDRESS],
#              customers[1][PHONE], customers[1][STATUS], customers[1][CREDIT_LIMIT])

# add_customer(customers[2][CUST_ID], customers[2][NAME], customers[2][LAST_NAME],
#              customers[2][HOME_ADDRESS], customers[2][EMAIL_ADDRESS],
#              customers[2][PHONE], customers[2][STATUS], customers[2][CREDIT_LIMIT])

print(list_active_customers())