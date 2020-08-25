# pylint: disable=W0614
# pylint: disable-msg=R0913
"""lesson 3 michael mcdonald """

import uuid
import sqlite3
import logging
import sys
# pylint: disable=wildcard-import
import peewee as pw

# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('basic_operations.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Create some functional and unit tests for the model. Store them in the tests directory.
# Develop tests, and show some tests passing. Show other tests failing.
# general requirements, specific to three user types
# Your code should not trigger any warnings or errors from Pylint.


# initiate a new sqlite3 db
# pragmas={'foreign_keys': 1} recommended to avoid foreign key errors


class Connection:
    """connect to database"""

    database = pw.SqliteDatabase('customers.db', pragmas={'foreign_keys': 1})
    connection_result = ''
    try:
        database.connect()
        logger.info('connection successful')
        connection_result = 'connection successful'
    except sqlite3.Error as error:
        logger.error('sqlite3 connection error %s', error, exc_info=True)
        connection_result = 'connection failed'


class BaseModel(pw.Model):
    """create a db base model"""


    class Meta():
        """ add meta class"""
        my_connection = Connection()
        database = my_connection.database


class Customer(BaseModel):
    """ customer model/table"""

    customer_id = pw.CharField(max_length=200, primary_key=True, null=False)
    name = pw.CharField(max_length=200, null=False)
    lastname = pw.CharField(max_length=200, null=False)
    home_address = pw.CharField(max_length=200, null=False)
    phone_number = pw.CharField(max_length=50, null=False)
    email_address = pw.CharField(max_length=200, null=False)
    status = pw.CharField(max_length=200, null=False)
    credit_limit = pw.IntegerField(default=0, null=False)  # int


try:
    my_connection = Connection()
    database = my_connection.database
    database.create_tables([Customer])
except sqlite3.Error as sqlerror:
    logger.error('error creating table %s', sqlerror, exc_info=True)


def is_digit(check_input):
    """function checking if your string is a pure digit, int  return : bool"""

    if check_input.isdigit():
        return True
    return False


def add_customer_handler():
    """add a new customer to the sqlite3 database"""

    try:
        status = ''
        customer_id = uuid.uuid1()  # create a unique customer id
        name = input('First name :')
        lastname = input('Last name:')
        home_address = input('Home address:')
        phone_number = input('Phone number:')
        email_address = input('Email address:')
        # active or inactive only
        # status = input('is the customer (a)ctive or (i)nactive?:').lower()
        is_status = False
        while not is_status:
            status = str(input('Is the customer (a)ctive or (i)nactive? >'))
            if status in ('i', 'a'):
                is_status = True
            else:
                print("Please enter a for active or i for inactive >")
        if status == 'a':
            status = 'active'
        elif status == 'i':
            status = 'inactive'

        credit_limit = input('What is their credit limit >')
        while not is_digit(credit_limit):
            print('Integers only')
            credit_limit = input('What is their credit limit >')
        add_customer(customer_id, name, lastname, home_address, phone_number,
                     email_address, status, credit_limit)
    except ValueError as e:
        logger.error('error creating inputs\t %e', e, exc_info=True)


def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """add new customer to database"""

    try:
        with database.transaction():
            tmp_customer = Customer.create(name=name, lastname=lastname, home_address=home_address,
                                           phone_number=phone_number, email_address=email_address,
                                           status=status, credit_limit=credit_limit,
                                           customer_id=customer_id)
            tmp_customer.save()
            for c in Customer.select().where(Customer.customer_id == customer_id):
                print('{}\t{}\t{} created'.format(c.customer_id, c.name, c.lastname))
            logger.info('customer %s created', customer_id)
    except sqlite3.Error as e:
        logger.error('error creating customer\t%s', e, exc_info=True)


def search_customer_handler():
    """ determine customer and call search_customer"""

    is_status = False
    while not is_status:
        customer_id = input('Please enter a customer id. Enter l to see a list of customers >')
        if customer_id == 'l'.lower():
            for c in Customer.select():
                print('{}\t{}\t{}'.format(c.customer_id, c.name, c.lastname))
        elif customer_id != 'l'.lower():
            tmp_customer = search_customer(customer_id)
            if len(tmp_customer) != 0:
                print('{}\t{}\t{}'.format(tmp_customer['customer_id'],
                                          tmp_customer['name'], tmp_customer['lastname']))
                results = '{}\t{}\t{}'.format(tmp_customer['customer_id'],
                                              tmp_customer['name'], tmp_customer['lastname'])
            else:
                print('{} not found'.format(customer_id))
                results = '{} not found'.format(customer_id)
            is_status = True
        else:
            print('Please enter a customer id. Enter l to see a list of customers >')
    return results


def search_customer(customer_id):
    """return a dictionary object with name, lastname, email address and phone number
    of a customer or an empty dictionary object if no customer was found."""

    results = {}
    try:
        # check first if exists
        tmp_customer = Customer.get_or_none(Customer.customer_id == customer_id)
        if tmp_customer is not None:
            results = {'name': tmp_customer.name, 'lastname': tmp_customer.lastname,
                       'home_address': tmp_customer.home_address,
                       'phone_number': tmp_customer.phone_number,
                       'email_address': tmp_customer.email_address,
                       'status': tmp_customer.status,
                       'credit_limit': tmp_customer.credit_limit,
                       'customer_id': tmp_customer.customer_id}
        if tmp_customer is None:
            logger.info('customer not found returned %s', customer_id, exc_info=True)
        return results  # just return an empty dictionary
    except IndexError:
        logger.error('IndexError thrown, error finding customer\t%s', customer_id, exc_info=True)
        print('customer not found')


def delete_customer_handler():
    """ determine customer and call delete_customer"""
    is_status = False
    while not is_status:
        customer_id = input('Enter the customer ID to be deleted. To see a list enter l >')
        if customer_id == 'l'.lower():
            for c in Customer.select():
                print('{}\t{}\t{}'.format(c.customer_id, c.name, c.lastname))
        elif customer_id != 'l'.lower():
            # check first if exists before passing to the delete method
            tmp_customer = Customer.get_or_none(Customer.customer_id == customer_id)
            if tmp_customer is None:
                print('- Customer not found - ')
                is_status = False
            if tmp_customer is not None:
                delete_customer(customer_id)
                is_status = True


def delete_customer(customer_id):
    """ delete a customer from the sqlite3 database"""

    tmp_customer = Customer.get(Customer.customer_id == customer_id)
    try:
        tmp_name = tmp_customer.name
        tmp_lastname = tmp_customer.lastname
        tmp_id = tmp_customer.customer_id
        c_to_del = Customer.get(Customer.customer_id == customer_id)
        c_to_del.delete_instance()
        logger.info('%s %s %s deleted successfully', tmp_name, tmp_lastname, tmp_id)
        print('{} {}, {} deleted successfully'.format(tmp_name, tmp_lastname, tmp_id))
    except sqlite3.Error as e:
        logger.error('delete customer error\t%s', e, exc_info=True)


def update_customer_credit_handler():
    """ determine customer and call update_customer_credit"""
    is_status = False
    while not is_status:
        customer_id = input('Enter the customer ID to be updated. To see a list enter l >')
        if customer_id == 'l'.lower():
            for c in Customer.select():
                print('{}\t{}\t{}'.format(c.customer_id, c.name, c.lastname))
        elif customer_id != 'l'.lower():
            # check first if exists before passing to the delete method
            tmp_customer = Customer.get_or_none(Customer.customer_id == customer_id)
            if tmp_customer is not None:
                new_credit_limit = input('Enter new credit limit >')
                while not is_digit(new_credit_limit):
                    print('Enter integers only')
                    new_credit_limit = input('Enter new credit limit >')
                update_customer_credit(customer_id, new_credit_limit)
                is_status = True
            if tmp_customer is None:
                print('- customer not found -')
                is_status = False


def update_customer_credit(customer_id, new_credit_limit):
    """search an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist"""

    try:
        query = Customer.update(credit_limit=new_credit_limit). \
            where(Customer.customer_id == customer_id)
        query.execute()
        logger.info('%s\tcredit updated\t new limit\t%s', customer_id, new_credit_limit)
        print('{} credit updated successfully. New limit {}'.format(customer_id, new_credit_limit))
    except sqlite3.Error as e:
        logger.error('update customer credit error\t%s', e, exc_info=True)


def list_active_customers():
    """list all active customers"""
    cust_cnt = Customer.select().where(Customer.status == 'active').count()
    for c in Customer.select().where(Customer.status == 'active'):
        print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(c.customer_id, c.name, c.lastname,
                                                  c.home_address, c.email_address,
                                                  c.status, c.credit_limit))
    return cust_cnt


def delete_all_customers():
    """delete all customers in database"""

    try:
        query = Customer.select()  # check for empty table
        if query.exists(None):
            for c in Customer.select():
                c_to_del = Customer.get(Customer.customer_id == c.customer_id)
                c_to_del.delete_instance(None)
                logger.info('%s\tdeleted', c.customer_id)
            print('all customers deleted. good luck on your next job.')
        else:
            print('Customer tables is already empty')
    except sqlite3.Error as e:
        logger.error('error deleting customers\t%s', e, exc_info=True)


def main_menu(user_prompt=None):
    """main menu"""

    valid_prompts = {'1': add_customer_handler,
                     '2': search_customer_handler,
                     '3': delete_customer_handler,
                     '4': update_customer_credit_handler,
                     '5': list_active_customers,
                     '6': delete_all_customers,
                     'q': exit_program}
    while user_prompt not in valid_prompts:
        print('Please choose from the following options ({options_str}):')
        print('1. Add customer')
        print('2. Search for a customer')
        print('3. Delete a customer')
        print('4. Update customer credit')
        print('5. List active customers')
        print('6. Delete all customers')
        print('q. Quit')
        user_prompt = input('>')
    return valid_prompts.get(user_prompt)


def insert_new_customers():
    """call and insert standard data as needed """
    with database.transaction():
        new_customers = [{'name': 'name3', 'lastname': 'lastname3',
                          'home_address': 'home_address3',
                          'phone_number': 'phone_number3',
                          'email_address': 'email_address3',
                          'status': 'active', 'credit_limit': 1000,
                          'customer_id': uuid.uuid1()},
                         {'name': 'name4', 'lastname': 'lastname4',
                          'home_address': 'home_address4',
                          'phone_number': 'phone_number4',
                          'email_address': 'email_address4',
                          'status': 'active', 'credit_limit': 1000,
                          'customer_id': uuid.uuid1()}, ]
        with database.atomic():
            Customer.insert_many(new_customers).execute()
    for customer in Customer.select():
        print('{}\t{}\t{}'.format(customer.customer_id, customer.name, customer.lastname))


def exit_program():
    """exit program"""

    sys.exit()


if __name__ == '__main__':
    print('running Lesson3 basic_operations')
    insert_new_customers()
    while True:
        main_menu()()
        input("Press Enter to continue...........")
