"""Norton db user input """

import sys
import os
import logging
import lesson5.database as mdb  # pylint: disable=import-error
from lesson5.database import ShowProductsAndCustomers  # pylint: disable=import-error

# set up logging
LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler('main_lesson_5.log')
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


def see_products_for_rent_handler():
    """Return a list of all products available for rent"""

    products = ShowProductsAndCustomers()
    my_list = products.see_products_for_rent()
    my_result_list = []
    for product in my_list:
        my_result_list.append(product)
        print(product)
    return my_result_list


def see_all_different_products_handler():
    """Return a list of all products available for rent"""

    products = ShowProductsAndCustomers()
    my_list = products.see_all_different_products()
    my_result_list = []
    for product in my_list:
        my_result_list.append(product)
        print(product)
    return my_result_list


def see_list_of_rental_details_handler():
    """Return a list of names and contact details"""

    is_status = False
    while not is_status:
        product_id = input('Please enter a product id. Enter l to see a list of products >')
        if product_id == 'l'.lower():
            products = ShowProductsAndCustomers()
            my_list = products.see_all_different_products()
            for product in my_list:
                print(product)
        elif product_id != 'l'.lower():
            products = ShowProductsAndCustomers()
            my_list = products.see_list_of_rental_details(product_id)
            if len(my_list) != 0:
                for product in my_list:
                    print(product)
                is_status = True
            else:
                print('{} not a product_Id'.format(product_id))
                is_status = False
        else:
            print('Please enter a customer id. Enter l to see a list of customers >')
    return product


def import_data_handler():
    """import customer, product and rental csv files"""

    result = ''
    try:
        current_dir = os.getcwd()
        directory_name = current_dir + '\\' + 'data' + '\\'
        file_name_dict = {'products': 'products.csv', 'customers': 'customers.csv',
                          'rentals': 'rentals.csv'}
        for key, value in file_name_dict.items():
            tmp_file = directory_name + value
            mongo_insert = mdb.ImportData(key, tmp_file)
            result = mongo_insert.import_data()
            print(result)
    except FileNotFoundError as e:
        logger.error('exception %s', e, exc_info=True)
        result = 'exception {}'.format(e)
        print(result)
    return result


def drop_data_handler():
    """drop data handler"""

    tables = ['customers', 'products', 'rentals']
    mongo_drop_table = mdb.DropData(tables)
    result = mongo_drop_table.drop_table()
    print(result)
    return result


def main_menu(user_prompt=None):
    """main menu"""

    valid_prompts = {'1': see_products_for_rent_handler,
                     '2': see_all_different_products_handler,
                     '3': see_list_of_rental_details_handler,
                     '4': import_data_handler,
                     '5': drop_data_handler,
                     'q': exit_program}
    while user_prompt not in valid_prompts:
        print('Please choose from the following options ({options_str}):')
        print('1. See a list of all products available for rent')
        print('2. See a list of different products')
        print('3. See a list of rental details by product')
        print('4. Import data')
        print('5. Drop data')
        print('q. Quit')
        user_prompt = input('>')
    return valid_prompts.get(user_prompt)


def exit_program():
    """exit program"""

    sys.exit(1)


if __name__ == '__main__':
    while True:
        main_menu()()
        input("Press Enter to continue...........")
