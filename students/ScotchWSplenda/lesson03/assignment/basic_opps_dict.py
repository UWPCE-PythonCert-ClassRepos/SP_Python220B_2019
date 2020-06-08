"""
who don't i have to 'connect' or 'close'?
"""

from customer_model import db, Customer
import peewee
import logging


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
#
Customer.drop_table()
Customer.create_table()


def add_customer(_name, _last_name, _home_address, _phone_number,
                 _email_address, _status, _poverty_score):
    '''add new customer function.'''
    try:
        with db.transaction():
            new_customer = Customer.create(
                        name=_name,
                        last_name=_last_name,
                        home_address=_home_address,
                        phone_number=_phone_number,
                        email_address=_email_address,
                        status=_status,
                        poverty_score=_poverty_score
                        )
            new_customer.save()
    except peewee.IntegrityError:
        LOGGER.warning("Customer Name %s is already taken.", _name)


def delete_customer(_name):
    '''Delete a customer from the customer database.'''
    with db.transaction():
        to_delete = Customer.get_or_none(Customer.name == _name)
        if to_delete is not None:
            to_delete.delete_instance()
        if to_delete is None:
            LOGGER.warning('Customer %s does not exist', _name)


def search_customer(name):
    '''Return a dictionary'''
    '''locate customer by id and return as dictionary.'''
    try:
        result = Customer.select().where(Customer.name == name).dicts().get()
    except peewee.DoesNotExist:
        result = {}
    return result


def update_customer_credit(name, credit_limit):
    '''update a customers credit limit by id.'''
    try:
        customer = Customer.get(Customer.name == name)
        customer.poverty_score = credit_limit
        customer.save()
    except peewee.DoesNotExist:
        LOGGER.warning('Customer %s does not exist', name)


def list_active_customers():
    '''list number of active customers.'''
    return Customer.select().where(Customer.status == True).count()

# 
# print(list_active_customers())
# customer1 = {
#     '_name': 'Freddie',
#     '_last_name': 'Gibbs',
#     '_home_address': '123 Fake St',
#     '_phone_number': '206-360-4200',
#     '_email_address': 'fgibbs@washington.edu',
#     '_status': True,
#     '_poverty_score': 420
#     }
#
# add_customer(**customer1)
# print(search_customer('Freddie'))
# print(list_active_customers())
