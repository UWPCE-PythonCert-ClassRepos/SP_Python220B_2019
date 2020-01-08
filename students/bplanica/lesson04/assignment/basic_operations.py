"""Basic operations utilizing the customer_model"""

import logging
import peewee as pw
from customer_model import Customer, DATABASE

# toggle below comment when needed
DATABASE.drop_tables([Customer])
DATABASE.create_tables([Customer])
#DATABASE.close()

def setup_logging():
    """setup file and console logging"""
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
    log_file = "db.log"

    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def add_customer(name, lastname, home_address, phone_number, email_address,
                 status, credit_limit):
    """create a new customer object in the database table"""
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(
                name=name,
                lastname=lastname,
                home_address=home_address,
                phone_number=phone_number,
                email_address=email_address,
                status=status,
                credit_limit=credit_limit)
            new_customer.save()
            logging.info("Database add successful: %s: %s %s", new_customer.customer_id,
                         name, lastname)
            return new_customer
    except pw.IntegrityError as exc:
        logging.info("Error creating %s; Exception: %s", name, exc)


def search_customer(customer_id):
    """search for an exisitng customer object in the database table"""
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        a_customer_info = {'name': a_customer.name,
                           'lastname': a_customer.lastname,
                           'phone_number': a_customer.phone_number,
                           'email_address': a_customer.email_address}
        logging.info(a_customer_info)
        return a_customer_info
    except pw.DoesNotExist:
        a_customer_info = {}
        logging.info(a_customer_info)
        return a_customer_info


def search_all_customers():
    """search for an exisitng customer object in the database table"""
    all_customers = []
    iterator = iter(Customer)
    while True:
        try:
            i = next(iterator)
        except StopIteration:
            break
        all_customers.append(search_customer(i))
    return all_customers


def delete_customer(customer_id):
    """delete an exiting customer object from the database table"""
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        fullname = f"{a_customer.name} {a_customer.lastname}"
        a_customer.delete_instance()
        logging.info("Database delete successful: %s: %s", customer_id, fullname)
    except pw.DoesNotExist:
        logging.info('Customer ID provided does not exist')


def update_customer_credit(customer_id, credit_limit):
    """update the credit limit for an existing customer"""
    try:
        a_customer = Customer.get(Customer.customer_id == customer_id)
        a_customer.credit_limit = credit_limit
        a_customer.save()
        logging.info("Database update successful: %s: %s %s; %s new credit limit",
                     a_customer.customer_id, a_customer.name, a_customer.lastname,
                     a_customer.credit_limit)
    except pw.DoesNotExist:
        logging.info('Customer ID provided does not exist')


def list_active_customers():
    """list all active customer: status = 1 (Active), status = 0 (Inactive)"""
    active_count = 0
    for _ in Customer.select().where(Customer.status):
        active_count += 1

    logging.info("Total active customers: %d", active_count)
    return active_count


if __name__ == "__main__":
    setup_logging()
