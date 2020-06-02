import logging
from peewee import *
from customer_model import Customer, DB

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(name, lastname, home_address, phone_number,
                 email_address, status, poverty_score):
    '''atomic() is easier than transaction()'''
    try:
        with DB.atomic():
            Customer.create(
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=poverty_score
            )
    except IntegrityError:
        LOGGER.warning("Name %s is already taken.", name)


def search_customer(find_name):
    '''locate customer by name'''
    try:
        result = Customer.select().where(Customer.name == find_name).dicts().get()
    except DoesNotExist:
        result = f'{find_name} does not exist'
    return result

# http://docs.peewee-orm.com/en/latest/peewee/query_examples.html?highlight=delete#delete-a-member-from-the-cd-members-table
def delete_customer(delete_name):
    '''delete a customer by id.'''
    try:
        with DB.atomic():
            Customer.delete().where(Customer.name == delete_name).execute()
            result = f'Succesfully deleted {delete_name}'
    except IntegrityError:
        result = f'{delete_name} does not exist'
    return result


# http://docs.peewee-orm.com/en/latest/peewee/query_builder.html?highlight=update#update-queries
def update_customer_credit(name, credit_limit):
    try:
        Customer.update(poverty_score=credit_limit).where(Customer.name == name).execute()
        result = f'{name} now has a credit score of {credit_limit}'
    except DoesNotExist:
        result = f'{name} does not exist'
    return result


# http://docs.peewee-orm.com/en/latest/peewee/query_examples.html#count-the-number-of-facilities
def list_active_customers():
    '''return an integer with the number of customers status is active.'''
    Customer.select().where(Customer.status == 1).count()
