"""
Functions to modify customer information in the customers.db table.
"""
import logging
from peewee import JOIN, DoesNotExist
import create_db
import customer_model as cm


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
create_db.main()


def add_customer(customer_id, name, lastname, home_address, phone_number, email_address, active, credit_limit):
    """
    Adds a customer to the database. Must have all parameters set for full customer record.

    :param customer_id: Customer identification number
    :param name: First name
    :param lastname: Last name
    :param home_address: Home address of customer
    :param phone_number: Phone number of customer
    :param email_address: Email address of current customer
    :param active: Boolean of customer status
    :param credit_limit: Customer's credit limit
    :return: None
    """
    try:
        with cm.database.transaction():
            contact_id = cm.Identity.create(
                customer_id=customer_id,
                name=name,
                last_name=lastname,
                credit_limit=credit_limit,
                active=active
            )
            contact_id.save()
        LOGGER.info(f"Succesfully added record to Identity {contact_id.customer_id}: {contact_id.last_name}")

    except Exception as e:
        LOGGER.info(f'Error creating = {customer_id}: {name} {lastname}')
        LOGGER.info(e)

    try:
        with cm.database.transaction():
            contact_info = cm.Contact.create(
                home_address=home_address,
                email_address=email_address,
                phone_number=phone_number,
                customer_id=customer_id
            )
            contact_info.save()

            LOGGER.info(f"Contact updated successfully with {contact_info.customer_id}: {contact_info.home_address}")

    except Exception as e:
        LOGGER.info(f'Error creating = {customer_id}: {home_address}')
        LOGGER.info(e)


def search_customer(customer_id):
    """
    Finds a customer information based on their
    :param customer_id:
    :return:
    """
    customer_info = dict()
    try:
        with cm.database.transaction():
            customer = cm.Identity \
                .select(cm.Identity, cm.Contact) \
                .join(cm.Contact, JOIN.INNER) \
                .where(cm.Contact.customer_id == customer_id) \
                .get()

        customer_info['name'] = customer.name
        customer_info['lastname'] = customer.last_name
        customer_info['email_address'] = customer.contact.email_address
        customer_info['phone_number'] = customer.contact.phone_number

    except DoesNotExist:
        LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")

    return customer_info


def delete_customer(customer_id):
    """
    Deletes a customer record and all associated information
    based on the input of their customer identification number.
    :param customer_id: Customer Identification number
    :return: None
    """

    try:
        with cm.database.transaction():
            customer = cm.Identity \
                .select(cm.Identity.customer_id) \
                .where(cm.Identity.customer_id == customer_id) \
                .get()

            customer.delete_instance(recursive=True)
        LOGGER.info("Successfully deleted user from database.")

    except DoesNotExist:
        LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")
        raise ValueError("Customer ID does not exist")


def update_customer_credit(customer_id, credit_limit):
    """
    Adjusts the credit limit for a customer specified by their
    customer identification number.

    :param customer_id: Customer id to increase limit
    :param credit_limit: Number to adjust credit limit to
    :return:
    """

    try:
        with cm.database.transaction():
            customer = (cm.Identity
                        .select()
                        .where(cm.Identity.customer_id == customer_id)
                        .get())

            LOGGER.info(f"Updating {customer.name} {customer.last_name} with credit limit {credit_limit}")
            customer.credit_limit = credit_limit
            customer.save()
            LOGGER.info(f"Updated {customer.name} {customer.last_name} credit limit to: {customer.credit_limit}")

    except DoesNotExist:
        LOGGER.warning(f"The customer ID {customer_id} does not exist in the database")
        raise ValueError("User Does not exist")



def list_active_customers():
    """
    Checks the Identity table of the database and counts the number
    of active customers. Value must equal 1 in the 'active' column.
    :return: number of active customers
    """
    try:
        with cm.database.transaction():
            active_customers = (cm.Identity
                                .select()
                                .where(cm.Identity.active == 1)
                                .count())

    except Exception as e:
        LOGGER.warning(f"Unable to determine active customers due to:\n {e}")

    return active_customers
