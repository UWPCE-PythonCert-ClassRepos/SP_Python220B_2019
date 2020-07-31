'''module to adjust data in Customer database'''
import logging
import peewee
from customer_model import db, Customer


LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.INFO)
CONSOLE_HANDLER.setFormatter(FORMATTER)


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)


def add_customer(customer_id, firstname, lastname, home_address,
                 phone_number, email_address, status, credit_limit):
    '''Add a new customer and related data to the customer database'''

    LOGGER.info(f"Adding a {firstname} {lastname} to Customer table")

    try:
        new_customer = Customer.create(customer_id=customer_id,
                                       first_name=firstname,
                                       last_name=lastname,
                                       home_address=home_address,
                                       phone_number=phone_number,
                                       email_address=email_address,
                                       status=status,
                                       credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info(f"{firstname} {lastname} added to customers.db")
    except peewee.IntegrityError:
        LOGGER.error(f'Unique customer_id required. {customer_id} not added')


def search_customer(customer_id):
    '''Search and retrieve info for customer_id'''
    LOGGER.info(f'Searching for customer ID {customer_id}')
    customer_dict = {}

    try:
        cust_data = Customer.get(Customer.customer_id == customer_id)
        customer_dict[customer_id] = [
            cust_data.first_name, cust_data.last_name, cust_data.email_address,
            cust_data.phone_number]
    except peewee.DoesNotExist:
        LOGGER.error(f'Customer ID {customer_id} not found.')

    return customer_dict


def delete_customer(customer_id):
    '''delete customer_id info from database'''
    LOGGER.info(f'Deleting customer ID {customer_id} from Customer table')
    with db.transaction():
        try:
            del_cust = Customer.get(Customer.customer_id == customer_id)
            del_cust.delete_instance()
            del_cust.save()
        except Customer.DoesNotExist as error_message:
            LOGGER.error(f'Customer {customer_id} not found. {error_message}')
            raise ValueError


def update_customer_credit(customer_id, credit_limit):
    '''Change customers credit limit'''
    LOGGER.info(f'Updating customer ID {customer_id} credit limit')
    try:
        cust_update01 = Customer.get(Customer.customer_id == customer_id)
        cust_update01.credit_limit = credit_limit
        cust_update01.save()
    except peewee.DoesNotExist as error_message:
        LOGGER.error(f'Customer ID {customer_id} not found. {error_message}')
        raise ValueError


def list_active_customers():
    '''Return integer with quantity of customers currently active'''
    active_customers = int(Customer.select().
                           where(Customer.customer_status).count())
    LOGGER.info(f'Quantity of active customers: {active_customers}')
    return active_customers


if __name__ == '__main__':
    db.create_tables([Customer])
    add_customer('001', 'Tony', 'Tentoes', '123 Elm St Springfield, CT 03821',
                 '321-555-1234', 'tt@email.com', True, 550)
    add_customer('002', 'Su', 'Sands', '987 Birch St Dover, CA 90387',
                 '789-555-4321', 'su@email.com', True, 700)
    add_customer('003', 'Pat', 'Smalls', '456 Pine St Smithburg, NM 67265',
                 '654-555-7531', 'pats@email.com', True, 375)
    print(search_customer('002'))
    print(search_customer('765'))
    list_active_customers()
    delete_customer('001')
    search_customer('001')
    update_customer_credit(customer_id='003', credit_limit=425)
    list_active_customers()
