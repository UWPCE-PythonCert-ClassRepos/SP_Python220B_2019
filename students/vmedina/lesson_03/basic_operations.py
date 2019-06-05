"""
Module that includes operations on the customers database
"""
# pylint: disable= W0401,W1202
import logging
import peewee
from HP import Customer


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def add_customer(customer_id, name, last_name, home_address, phone_number, email_address, status,
                 credit_limit):
    """
    :param customer_id:
    :type customer_id:
    :param name:
    :type name:
    :param last_name:
    :type last_name:
    :param home_address:
    :type home_address:
    :param phone_number:
    :type phone_number:
    :param email_address:
    :type email_address:
    :param status:
    :type status:
    :param credit_limit:
    :type credit_limit:
    :return:
    :rtype:
    """
    try:
        new_customer = Customer.create(customer_id=customer_id,
                                       customer_name=name,
                                       customer_last_name=last_name,
                                       home_address=home_address,
                                       phone_number=phone_number,
                                       email_address=email_address,
                                       status=status,
                                       credit_limit=int(credit_limit))
        new_customer.save()
        LOGGER.info('Added a new customer')

    except peewee.IntegrityError as error:
        LOGGER.info('Customer with ID {} could not be created, check all inputs'
                    .format(customer_id))
        LOGGER.info(error)


def search_customer(customer_id):
    """

    :param customer_id:
    :type customer_id:
    :return:
    :rtype:
    """
    try:
        customer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info('Found customer with id {} '.format(customer_id))
        customer_info = {'name': customer.customer_name,
                         'last_name': customer.customer_last_name,
                         'email_address': customer.email_address,
                         'phone_number': customer.phone_number}
        return customer_info
    except IndexError as error:
        LOGGER.info("Could not find customer with id {}".format(customer_id))
        LOGGER.info(error)
        return {}

    return {}


def delete_customer(customer_id):
    """

    :param customer_id:
    :type customer_id:
    :return:
    :rtype:
    """
    LOGGER.info('Deleting customer with id {}'.format(customer_id))
    customer = Customer.get(Customer.customer_id == customer_id)
    try:
        customer.delete_instance()
    except IndexError as index_error:
        LOGGER.info("Customer with id {} doesn't exist".format(customer_id))
        LOGGER.info(index_error)




def update_customer_credit(customer_id, credit_limit):
    """

    :param customer_id:
    :type customer_id:
    :param credit_limit:
    :type credit_limit:
    :return:
    :rtype:
    """

    customer = Customer.get(Customer.customer_id == customer_id)
    LOGGER.info('Credit limit before the change is {}'.format(customer.credit_limit))
    customer.credit_limit = int(credit_limit)
    customer.save()
    LOGGER.info('New credit limit is {}'.format(customer.credit_limit))


def list_active_customers():
    """
    :return:
    :rtype:
    """
    query = Customer.select().where(Customer.status == True).count()
    return query
