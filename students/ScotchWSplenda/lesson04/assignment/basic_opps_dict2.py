"""
who don't i have to 'connect' or 'close'?
"""

from customer_model import db, Customer
import peewee
import logging
import datetime

# tell logger where to save
LOG_FILE = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
FH = logging.FileHandler(LOG_FILE)
# tell logger how to save each row
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
FH.setFormatter(FORMATTER)
# get that fucker going
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FH)

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
            LOGGER.info("Added customer %s %s to database.", _name, _last_name)
    except peewee.IntegrityError:
        LOGGER.warning("Customer %s %s is already taken.", _name, _last_name)


# def delete_customer(_name):
#     '''Delete a customer from the customer database.'''
#     with db.transaction():
#         to_delete = Customer.get_or_none(Customer.name == _name)
#         result = [Customer.select().where(Customer.name == _name).dicts().get()]
#         result2 = ' '.join([y['name'] +' '+ y['last_name'] for y in result])
#         if to_delete is not None:
#             to_delete.delete_instance()
#             LOGGER.info("Deleted %s", result2)
#         if to_delete is None:
#             LOGGER.warning('Customer %s does not exist', _name)

def delete_customer(_name):
    '''Delete a customer from the customer database.'''
    with db.transaction():
        result = Customer.get(Customer.name == _name)
        if result is not None:
            result.delete()
            LOGGER.info("Deleted %s %s", result.name, result.last_name)
        if result is None:
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
    # return Customer.select().where(Customer.status == True).count()
    return 'Your DB has: '+ ', '.join([x.name +' '+ x.last_name for x in Customer.select()])
    # return ' '.join([y['name'] +' '+ y['last_name'] for y in result])
