"""lesson8 partials and closures"""

# pylint: disable=E1111
# pylint: disable=import-error
# pylint: disable=W0614
# pylint: disable-msg=R0913
# pylint: disable-msg=too-many-locals
# pylint: disable-msg=too-many-statements
import csv
import sys
import os
import os.path
import random
from functools import partial
from lesson8 import generate_csv


INVOICE_FILE = 'invoice_file.csv'
FIXED_CUSTOMER_NAME = 'Emily Blunt'


def csv_file():
    """create full file name from current directory"""

    input_file_local = INVOICE_FILE
    current_dir = os.getcwd()
    results = current_dir + '\\' + input_file_local
    return results


def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    """ create csv invoice_file"""

    if os.path.isfile(invoice_file):
        add_to_csv_file = generate_csv.BuildCsvFile(invoice_file,
                                                    customer_name,
                                                    item_code,
                                                    item_description,
                                                    item_monthly_price)
        add_to_csv_file.add_rows()
    else:
        open(invoice_file, 'w+')
        add_to_csv_file = generate_csv.BuildCsvFile(invoice_file,
                                                    customer_name,
                                                    item_code,
                                                    item_description,
                                                    item_monthly_price)
        add_to_csv_file.add_rows()


def add_furniture_handler():
    """a helper function to quickly add furniture"""

    invoice_file = csv_file()
    customer_name_list = ['Tom Hanks', 'Dwayne Johnson', 'Leonardo DiCaprio', 'Will Smith',
                          'Matt Damon', 'Emma Watson', 'Anne Hathaway', 'Angelina Jolie',
                          'Emma Stone', 'Sandra Bullock']
    items_list = [['WFT', 'Woodlands Friendship Table', 4000],
                  ['WDCT', 'Winnie Demilune Console Table', 2000],
                  ['SWNST', 'Its A Small Wonder Night Stand', 1500],
                  ['CBC', 'Charmant Bachelorette Chest', 6000],
                  ['SC', 'Sullivan Credenza', '2,500'],
                  ['LSC', 'Lilith Side Chairs (pair)', 3000]]
    customer_name = random.choice(customer_name_list)
    random_item = random.randrange(0, 4, 1)
    item_code = items_list[random_item][0]
    item_description = items_list[random_item][1]
    item_monthly_price = items_list[random_item][2]
    print(customer_name, item_code, item_description, item_monthly_price)
    add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price)


def single_customer_handler():
    """ call single customer with arguments"""

    current_dir = os.getcwd()
    rental_file_local = current_dir + '\\' + 'rental_items.csv'
    invoice = single_customer(FIXED_CUSTOMER_NAME, INVOICE_FILE)
    invoice(rental_file_local)
    print('Invoice Created')


def single_customer(customer_name, invoice_file):
    """Returns a function that takes one parameter, rental_items
    Output: Returns a function that takes one parameter, rental_items
    """

    def create_invoice_file(rental_items):
        tmp_partial_fn = partial(add_furniture, invoice_file, customer_name)
        with open(rental_items) as read_obj:
            csv_reader = csv.reader(read_obj)
            for item in csv_reader:
                tmp_partial_fn(item[0], item[1], item[2])
    return create_invoice_file


def delete_furniture_handler():
    """delete the invoice file"""

    input_file_local = csv_file()
    if os.path.exists(input_file_local):
        os.remove(input_file_local)
        print('Invoice file deleted')
    else:
        print('Invoice file does not exist')


def exit_program():
    """exit program"""

    sys.exit(1)


def main_menu(user_prompt=None):
    """main menu"""

    valid_prompts = {'1': add_furniture_handler,
                     '2': single_customer_handler,
                     '3': delete_furniture_handler,
                     'q': exit_program}
    while user_prompt not in valid_prompts:
        print('Please choose from the following options ({options_str}):')
        print('1. Add to Inventory')
        print('2. Run Single Customer Function')
        print('3. Delete Inventory File')
        print('q. Quit')
        user_prompt = input('>')
    return valid_prompts.get(user_prompt)


if __name__ == "__main__":
    while True:
        main_menu()()
        input("Press Enter to continue...........")
