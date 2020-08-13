"""
    Customer database with Peewee ORM, sqlite and Python
    Here we define the database operations
"""
import logging
import peewee
from customer_model import database, Customer


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a logging "formatter"
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

# Create a log message handler that sends output to log_file
file_handler = logging.FileHandler('db.log', mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create a log message handler that sends output to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


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
    logger.info('In function add_customer...')
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
        list_customers()
    except (peewee.IntegrityError, peewee.OperationalError):
        logger.info(f'Error adding customer {customer_id}')
    finally:
        database.close()


def search_customer(customer_id):
    """
    look up a customer and return a dictionary object with customer information
    or an empty dictionary object if no customer was found
    """
    logger.info('In function search_customer...')
    customer_info = {}
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)

        customer_info['name'] = a_customer.name
        customer_info['last name'] = a_customer.last_name
        customer_info['email address'] = a_customer.email_address
        customer_info['phone number'] = a_customer.phone_number

        logger.info(f'Customer {customer_id} info returned.')
    except peewee.DoesNotExist:
        logger.info(f'Customer {customer_id} not found.')
    finally:
        database.close()

    return customer_info


def delete_customer(customer_id):
    """ delete a customer from the database """
    logger.info('In function delete_customer...')
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)
            a_customer.delete_instance()
        logger.info(f'Customer {customer_id} deleted.')
        list_customers()
    except peewee.DoesNotExist:
        logger.info(f'Customer {customer_id} not found.')
    finally:
        database.close()


def update_customer_credit(customer_id, credit_limit):
    """
    search an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist
    """
    logger.info('In function update_customer_credit...')
    try:
        with database.transaction():
            a_customer = Customer.get(Customer.customer_id == customer_id)
        logger.info(f'Customer {customer_id} credit limit is '
                    f'{a_customer.credit_limit}.')
    except (IndexError, ValueError, peewee.DoesNotExist):
        logger.info(f'Customer {customer_id} not found.')
        database.close()
        return

    with database.transaction():
        query = (Customer
                 .update({Customer.credit_limit: credit_limit})
                 .where(Customer.customer_id == customer_id))
        query.execute()

        a_customer = Customer.get(Customer.customer_id == customer_id)

    logger.info(f'Customer {customer_id} credit limit is updated to '
                f'{a_customer.credit_limit}.')
    list_customers()
    database.close()


def list_active_customers():
    """
    return an integer with the number of customers whose status is
    currently active
    """
    logger.info('In function list_active_customers...')
    count = None

    with database.transaction():
        count = Customer.select().where(Customer.active).count()
    logger.info(f'active customer count = {count}')
    database.close()

    return count


def list_customers():
    """ list all customers in the database """
    logger.info('List all customers in the current database')
    display_header = f"{'ID':5}{'Name':20}{'Phone No':15}{'Email':30}" \
                     f"{'Active':<8}{'Credit Limit':<12}"
    logger.info(display_header)
    logger.info('-'*90)

    for customer in customer_generator():
        row = f'{customer.customer_id:5}{customer.name:20}{customer.phone_number:15}' \
              f'{customer.email_address:30}{customer.active:<8}{customer.credit_limit:<12}'
        logger.info(row)


def customer_generator():
    """ generator to get one customer at a time """
    with database.transaction():
        all_customers = Customer.select()
    for customer in all_customers:
        yield customer
