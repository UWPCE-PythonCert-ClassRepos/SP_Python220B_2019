'''
Basic opertions

'''

from customers_model import *
from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#database = SqliteDatabase('customers.db')


def add_customer(customer_id, name, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    try:
        #database.connect()
        #database.execute_sql('PRAGMA foreign_keys = On;')
        with database.transaction():
            new_customer = Customers.create(
                customer_id = customer_id,
                name = name,
                lastname = lastname,
                home_address = home_address,
                phone_number = phone_number,
                email_address = email_address,
                status = status,
                credit_limit = credit_limit
            )
            new_customer.save()
            logger.info('Database add successful')
    except Exception as e:
        logger.info('Error creating = {}'.format(name))
        logger.info(e)
    finally:
        database.close()
        logger.info('Database closed')
        

def search_customer(customer_id):
    '''Insert docstring'''
    try:
        customer = Customers.get(Customers.customer_id == customer_id)
        #name, lastname, email address and phone number
        logger.info('Customer found')
        return {'name':customer.name, 'lastname':customer.lastname,
                'email_address':customer.email_address, 'phone_number':customer.phone_number}
    except DoesNotExist as e:
        logger.info(e)
        return {}   



def delete_customer(customer_id):
    pass

def update_customer_credit(customer_id, credit_limit):
    pass

def list_active_customers():
    pass


if __name__ == "__main__":
    database.create_tables([Customers])
    database.close()



