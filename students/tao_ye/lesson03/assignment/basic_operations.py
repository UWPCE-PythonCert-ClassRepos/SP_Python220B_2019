"""
    Customer database with Peewee ORM, sqlite and Python
    Here we define the database operations
"""
import logging
import peewee
from customer_model import database, Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create the customer table in the database
def create_customer_table():
    """ create Customer table if not exists """
    with database:
        Customer.create_table()
    logger.info('Customer table create successful')
    database.close()


def add_customer(customer_id, name, last_name, home_address, phone_number,
                 email_address, active, credit_limit):
    """ add a new customer to the database """
    try:
        with database.transaction():
            new_customer = Customer.create(
                customer_id=customer_id,
                name=name,
                last_name=last_name,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                active=active,
                credit_limit=credit_limit)
            new_customer.save()
        logger.info(f'Customer {customer_id} add successful')
    except (peewee.IntegrityError, peewee.OperationalError):
        logger.info(f'Error adding customer: {customer_id}')
    finally:
        database.close()


def search_customer(customer_id):
    """
    look up a customer and return a dictionary object with customer information
    or an empty dictionary object if no customer was found
    """
    customer_info = {}
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)

        customer_info['name'] = a_customer.name
        customer_info['last name'] = a_customer.last_name
        customer_info['email address'] = a_customer.email_address
        customer_info['phone number'] = a_customer.phone_number

        logger.info(f'Customer: {customer_id} info returned.')
    except peewee.DoesNotExist:
        logger.info(f'Customer: {customer_id} not found.')
    finally:
        database.close()

    return customer_info


def delete_customer(customer_id):
    """ delete a customer from the database """
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)
            a_customer.delete_instance()
        logger.info(f'Customer: {customer_id} deleted.')
    except peewee.DoesNotExist:
        logger.info(f'Customer: {customer_id} not found.')
    finally:
        database.close()


def update_customer_credit(customer_id, credit_limit):
    """
    search an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist
    """
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'Customer: {customer_id} credit limit is '
                    f'{a_customer.credit_limit}.')
    except (IndexError, ValueError, peewee.DoesNotExist):
        logger.info(f'Customer: {customer_id} not found.')
        database.close()
        return

    with database.transaction():
        query = (Customer
                 .update({Customer.credit_limit: credit_limit})
                 .where(Customer.customer_id == customer_id))
        query.execute()

        a_customer = Customer.get(Customer.customer_id == customer_id)

    logger.info(f'Customer: {customer_id} credit limit is updated to '
                f'{a_customer.credit_limit}.')
    database.close()


def list_active_customers():
    """
    return an integer with the number of customers whose status is
    currently active
    """
    count = None

    with database.transaction():
        count = Customer.select().where(Customer.active).count()
    logger.info(f'active customer count: {count}')
    database.close()

    return count
