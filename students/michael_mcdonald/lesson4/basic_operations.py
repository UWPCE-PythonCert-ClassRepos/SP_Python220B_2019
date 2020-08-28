# pylint: disable=W0614
# pylint: disable-msg=R0913
"""lesson 4 michael mcdonald """

import uuid
import sqlite3
import logging
import sys
import operator
# pylint: disable=wildcard-import
from functools import reduce
import peewee as pw


# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('basic_operations.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
sql_file_handler = logging.FileHandler('db.log')
sql_file_handler.setLevel(logging.INFO)
sql_file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

sql_logger = logging.getLogger('peewee')
sql_logger.addHandler(logging.StreamHandler())
sql_logger.setLevel(logging.INFO)
sql_logger.addHandler(sql_file_handler)
sql_logger.addHandler(console_handler)


# initiate a new sqlite3 db
# pragmas={'foreign_keys': 1} recommended to avoid foreign key errors
database = pw.SqliteDatabase('customers.db', pragmas={'foreign_keys': 1})
try:
    database.connect()
except sqlite3.Error as sqlerror:
    sql_logger.error('sqlite3 connection error %s', sqlerror, exc_info=True)


class Connection:
    """connect to database"""

    database = pw.SqliteDatabase('customers.db', pragmas={'foreign_keys': 1})
    connection_result = ''
    database.connect()
    connection_result = 'connection successful'


class BaseModel(pw.Model):
    """create a db base model"""

    class Meta():
        """ add meta class"""
        my_connection = Connection()
        database = my_connection.database


class Customer(BaseModel):
    """ customer model/table """

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
    sql_logger.error('error creating table %s', sqlerror, exc_info=True)

# helper functions and methods
def is_digit(check_input):
    """ function checking if your string is a pure digit, int  return : bool """

    if check_input.isdigit():
        return True
    return False


def to_proper_case(s):
    """ convert strings to Proper case """
    return str(s).title()


def add_tab(s):
    """ add tabs """
    return str(s) + '\t'


def add_header():
    """ add customer table header """
    header = 'CustomerID\tName\tLastname\tHome Address\tEmail Address\tStatus\tCredit Limit'
    print(header)


# use lambda & filter to print correct message
def user_messages(user_message_type):
    """ standardized messaging is generated based on the the request type """

    mess_dict = {'update_credit_success': '- customer credit updated successfully-',
                 'cust_delete_success': '- customer delete success -',
                 'del_all_customers': '- all customers deleted. good luck on your next job -',
                 'empty_customer_set': '- no customer(s) found -'}
    filtered_mess_list = dict(filter(lambda elem: elem[0] == user_message_type, mess_dict.items()))
    print(list(filtered_mess_list.values())[0])


# use map and reduce to simplify list management
def print_customer_data(customer_id='', name='', lastname='', home_address='',
                        email_address='', status='', credit_limit=''):
    """ create all print formatting here """

    tmp_id = '{}\t'.format(customer_id)
    tmp_list = [name, lastname, home_address, email_address, status, credit_limit]
    tmp_list = map(to_proper_case, tmp_list)
    tmp_list = list(map(add_tab, tmp_list))
    tmp_list.insert(0, tmp_id)  # add in customer_id
    tmp_list = reduce(operator.add, tmp_list)
    print(tmp_list)


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
            add_header()
            for c in Customer.select().where(Customer.customer_id == customer_id):
                print_customer_data(c.customer_id, c.name, c.lastname, c.home_address,
                                    c.email_address, c.status, c.credit_limit)
            sql_logger.info('customer %s created', customer_id)
    except sqlite3.Error as e:
        sql_logger.error('error creating customer\t%s', e, exc_info=True)


def search_customer_handler():
    """ determine customer and call search_customer"""

    is_status = False
    while not is_status:
        customer_id = input('Please enter a customer id. Enter l to see a list of customers >')
        if customer_id == 'l'.lower():
            add_header()
            for c in Customer.select():
                print_customer_data(c.customer_id, c.name, c.lastname, c.home_address,
                                    c.email_address, c.status, c.credit_limit)
        elif customer_id != 'l'.lower():
            c = search_customer(customer_id)
            add_header()
            if len(c) != 0:
                print_customer_data(c['customer_id'], c['name'], c['lastname'], c['home_address'],
                                    c['email_address'], c['status'], c['credit_limit'])
                results = '{}\t{}\t{}'.format(c['customer_id'],
                                              c['name'], c['lastname'])
            else:
                print('{} not found'.format(customer_id))
                results = '{} not found'.format(customer_id)
            is_status = True
        else:
            print('Please enter a customer id. Enter l to see a list of customers >')
    return results


def search_customer(customer_id):
    """ returns a dictionary of a customer or an empty dictionary if no customer found """

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
            sql_logger.info('customer not found returned %s', customer_id, exc_info=True)
        return results  # just return an empty dictionary
    except IndexError:
        logger.error('IndexError thrown, error finding customer\t%s', customer_id, exc_info=True)
        user_messages('empty_customer_set')


def delete_customer_handler():
    """ determine customer and call delete_customer"""
    is_status = False
    while not is_status:
        customer_id = input('Enter the customer ID to be deleted. To see a list enter l >')
        if customer_id == 'l'.lower():
            add_header()
            for c in Customer.select():
                print_customer_data(c.customer_id, c.name, c.lastname, c.home_address,
                                    c.email_address, c.status, c.credit_limit)
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

    try:
        c = Customer.get(Customer.customer_id == customer_id)
        sql_logger.info('%s %s %s deleted successfully', c.name, c.lastname, customer_id)
        user_messages('cust_delete_success')
        print_customer_data(c.customer_id, c.name, c.lastname, c.home_address, c.email_address,
                            c.status, c.credit_limit)
        c.delete_instance()
    except sqlite3.Error as e:
        sql_logger.error('delete customer error\t%s', e, exc_info=True)


def update_customer_credit_handler():
    """ determine customer and call update_customer_credit"""
    is_status = False
    while not is_status:
        customer_id = input('Enter the customer ID to be updated. To see a list enter l >')
        if customer_id == 'l'.lower():
            add_header()
            for c in Customer.select():
                print_customer_data(c.customer_id, c.name, c.lastname, c.home_address,
                                    c.email_address, c.status, c.credit_limit)
        elif customer_id != 'l'.lower():
            # check first if exists before passing to the delete method
            c = Customer.get_or_none(Customer.customer_id == customer_id)
            if c is not None:
                new_credit_limit = input('Enter new credit limit >')
                while not is_digit(new_credit_limit):
                    print('Enter integers only')
                    new_credit_limit = input('Enter new credit limit >')
                update_customer_credit(customer_id, new_credit_limit)
                is_status = True
            if c is None:
                user_messages('empty_customer_set')
                is_status = False


def update_customer_credit(customer_id, new_credit_limit):
    """search an existing customer by customer_id and update their credit limit
    or raise a ValueError exception if the customer does not exist"""

    try:
        query = Customer.update(credit_limit=new_credit_limit).\
            where(Customer.customer_id == customer_id)
        query.execute()
        c = Customer.get(Customer.customer_id == customer_id)
        user_messages('update_credit_success')
        add_header()
        print_customer_data(c.customer_id, c.name, c.lastname, c.home_address, c.email_address,
                            c.status, c.credit_limit)
        sql_logger.info('%s\tcredit updated\t new limit\t%s', customer_id, new_credit_limit)
    except sqlite3.Error as e:
        sql_logger.error('update customer credit error\t%s', e, exc_info=True)


def list_active_customers():
    """list all active customers using comprehension"""
    cust_cnt = Customer.select().where(Customer.status == 'active').count()
    add_header()
    for c in Customer.select().where(Customer.status == 'active'):
        print_customer_data(c.customer_id, c.name, c.lastname, c.home_address, c.email_address,
                            c.status, c.credit_limit)
    return cust_cnt


def delete_all_customers():
    """delete all customers in database"""

    try:
        customers = Customer.select()  # check for empty table
        if customers.exists(None):
            for c in Customer.select():
                c_to_del = Customer.get(Customer.customer_id == c.customer_id)
                c_to_del.delete_instance(None)
                sql_logger.info('%s\tdeleted', c.customer_id)
            user_messages('del_all_customers')
        else:
            user_messages('empty_customer_set')
    except sqlite3.Error as e:
        sql_logger.error('error deleting customers\t%s', e, exc_info=True)


def main_menu(user_prompt=None):
    """main menu"""

    valid_prompts = {"1": add_customer_handler,
                     "2": search_customer_handler,
                     "3": delete_customer_handler,
                     "4": update_customer_credit_handler,
                     "5": list_active_customers,
                     "6": delete_all_customers,
                     "7": insert_new_customers,
                     "q": exit_program}
    while user_prompt not in valid_prompts:
        print("Please choose from the following options ({options_str}):")
        print("1. Add customer")
        print("2. Search for a customer")
        print("3. Delete a customer")
        print("4. Update customer credit")
        print("5. List active customers")
        print("6. Delete all customers")
        print("7. Insert test customers")
        print("q. Quit")
        user_prompt = input(">")
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
    while True:
        main_menu()()
        input("Press Enter to continue...........")
