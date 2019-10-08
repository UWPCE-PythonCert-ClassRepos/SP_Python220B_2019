"""
This file contains functions required to perform different
operations on customer database
"""

from Customer_model import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

customers_list = [('Andrew', 'peterson', '344 james ave', 6308153728, 'a_peteerson@mail.com',1,4500),
                  ('Wang', 'Wou', '103 spring ave', 2223334456, 'wang_wou@gmail.com',0,22000)]
NAME = 0
LASTNAME = 1
ADDRESS = 2
PHONE = 3
EMAIL = 4
STATUS = 5
LIMIT = 6

status_dict = {1:'Active', 2:'NotActive'}

def add_customer():

    for c in customers_list:
        try:
            with db.transaction():
                logger.info(f'Adding \"{c[NAME]} {c[LASTNAME]}\" as new customer')
                new_customer = Customer.create(
                    name = c[NAME],
                    lastname = c[LASTNAME],
                    home_address = c[ADDRESS],
                    phone_number = c[PHONE],
                    email_address = c[EMAIL],
                    status = c[STATUS],
                    credit_limit = c[LIMIT])
                logger.info(f'New Customer : \"{c[NAME]} {c[LASTNAME]}\" added to the database')
                new_customer.save()

        except Exception as e:
            logger.info(f'Error adding  \"{c[NAME]} {c[LASTNAME]}\" as new Customer')
            logger.info(e)


def search_customer(id):
    """
    This function will return a dictionary object with name,
    lastname, email address and phone number of a customer or
    an empty dictionary object if no customer was found.
    """
    try:

        a_customer = Customer.get(Customer.id == id)
        a_customer_dict = {'id': a_customer.id,
                           'name': a_customer.name,
                           'last_name': a_customer.lastname,
                           'phone_number': a_customer.phone_number,
                           'email_address': a_customer.email_address,
                      }
        print (a_customer_dict)
        # return (a_customer_dict)

    except Exception as e:
         logger.info (f'No customer with id={id} was found')
         a_customer_dict = dict()
    return (a_customer_dict)



def del_customer(id):
    """
    This function will delete a customer from the sqlite3 database.
    """
    try:
        logger.info(f'Searching for customer with id = {id}')
        a_customer = Customer.get(Customer.id == id)
        logger.info (f'Deleting Cusotmer_ID = {id}, Customer_name = {a_customer.name}')
        a_customer.delete_instance()
        logger.info(f'customer {a_customer.name} with id = {id} deleted')

    except Exception as e:
        logger.info(f'No customer with id={id} was found')



def update_customer_credit(id, credit_limit):
    """
    This function will search an existing customer by customer_id and update their credit limit or raise a ValueError exception if the customer does not exist.
    :param customer_id:
    :param credit_limit:
    :return:
    """
    try:
        customer = search_customer(id)
        a_customer = Customer.get(Customer.id == id)
        logger.info(f'old credit limit = {a_customer.credit_limit}')
        a_customer.credit_limit = credit_limit
        logger.info(f'New credit limit = {a_customer.credit_limit}')
        return customer
    except Exception as e:
        logger.info(f'Cant update credit limit. No customer with id={id} was found')


def list_active_customers():
    """
    This function will return an integer with the number of customers whose status is currently active.
    :return:
    """
    # Can i use a query like this one ?
    # a_query = Customer.select(fn.COUNT(Customer.status)).where(Customer.status == True)


    active_customer_count = 0
    for customer in Customer.select():
        if customer.status == True:
            active_customer_count+=1
    return active_customer_count


if __name__ == '__main__':
    add_customer()
    print(list_active_customers())
    search_customer(1)
    print (search_customer(3))
    update_customer_credit(1, 25000)
    update_customer_credit(4, 35000)
    del_customer(4)

