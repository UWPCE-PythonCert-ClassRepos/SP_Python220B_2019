# pylint: disable=too-many-arguments
"""
Basic operations for customer model
"""
import logging
import peewee as pw
from customer_model import Customer, DB

# logging config
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, full_name, last_name, home_address, phone_number,
                 email_address, is_active, credit_limit):
    """Add a customer to the database"""
    try:
        Customer.create(customer_id=customer_id,
                        full_name=full_name,
                        last_name=last_name,
                        home_address=home_address,
                        phone_number=phone_number,
                        email_address=email_address,
                        is_active=is_active,
                        credit_limit=credit_limit)
    except pw.IntegrityError:
        LOGGER.critical("Cannot create record for ID '%s': already exists",
                        customer_id)
        raise ValueError


def search_customer(customer_id):
    """Get customer info from database for a given customer id"""
    # attempt to fetch given customer id; return None if not found
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
    except pw.DoesNotExist:
        LOGGER.info("ID not found: '%s'", customer_id)
        return None

    # if customer exists, return formatted data
    out_dict = {
        'full_name': customer.full_name,
        'last_name': customer.last_name,
        'email_address': customer.email_address,
        'phone_number': customer.phone_number,
    }
    return out_dict


def delete_customer(customer_id):
    """Delete a given customer id from the database"""
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        customer.delete_instance()
    except pw.DoesNotExist:
        LOGGER.error("Failed to delete ID '%s': not found in database",
                     customer_id)
        raise ValueError


def update_customer_credit(customer_id, credit_limit):
    """Update an existing customer's credit limit"""
    try:
        with DB.atomic():
            customer = Customer.get(Customer.customer_id == customer_id)
            customer.credit_limit = credit_limit
            customer.save()
    except pw.DoesNotExist:
        LOGGER.error("Failed to update ID '%s': not found in database",
                     customer_id)
        raise ValueError


def list_active_customers():
    """Return the number of customers where is_active is True"""
    return Customer.select().where(Customer.is_active).count()
