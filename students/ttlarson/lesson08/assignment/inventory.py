""" This module will add customer and items to a flat file database """
import os
import sys
import logging
from functools import partial
import pandas as pd

logging.basicConfig(level=logging.INFO)

# pylint: disable=invalid-name

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """
    This function will create invoice_file if it doesn’t exist or
    append a new line to it if it does.
    """
    file_path = get_file_full_path(invoice_file)
    df = read_data_df(file_path)
    row = [customer_name, item_code, item_description, item_monthly_price]
    df.loc[len(df)] = row
    df.drop_duplicates(inplace=True)
    df.to_csv(file_path, index=False, header=False)

def single_customer(customer_name, invoice_file):
    """ add one customer to data file """

    def add_rental_item(data_file):
        """ add rental items to data file """
        file_path = get_file_full_path(data_file)
        df = read_data_df(file_path)

        add_data_to_file = partial(add_furniture,
                                   invoice_file=invoice_file,
                                   customer_name=customer_name)

        for i, r in df.iterrows():
            add_data_to_file(item_code=r['item_code'],
                             item_description=r['item_description'],
                             item_monthly_price=r['item_monthly_price'])
            logging.info('''Adding item %d: item_code: %s,
                         item_description: %s,
                         item_monthly_price: %f''',
                         i,
                         r['item_code'],
                         r['item_description'],
                         r['item_monthly_price'])

    return add_rental_item

def read_data_df(data_file):
    """ read full path data file into a dataframe """
    print('Using data file: {}'.format(data_file))
    if not os.path.exists(data_file):
        open(data_file, 'w').close()

    if os.path.basename(data_file) == 'rented_items.csv':
        colnames = ['customer_name', 'item_code', 'item_description', 'item_monthly_price']
    elif os.path.basename(data_file) == 'test_items.csv':
        colnames = ['item_code', 'item_description', 'item_monthly_price']
    else:
        logging.info('Unknown data file ... exit processing.')
        sys.exit()

    try:
        df = pd.read_csv(data_file, names=colnames, header=None, sep=',')
    except OSError:
        logging.info('Cannot read file: %s.', data_file)
        df = pd.DataFrame()
        df.columns = ['customer_name', 'item_code', 'item_description', 'item_monthly_price']

    return df

def get_file_full_path(file_name):
    """ get data file full path using current the script file path """
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

if __name__ == '__main__':
    # main execution
    add_furniture('rented_items.csv', 'Elisa Miles', 'LR04', 'Leather Sofa', 25)
    add_furniture('rented_items.csv', 'Edward Data', 'KT78', 'Kitchen Table', 10)
    add_furniture('rented_items.csv', 'Alex Gonzales', 'BR02', 'Queen Mattress', 17)
    create_invoice = single_customer('Susan Wong', 'rented_items.csv')
    create_invoice(get_file_full_path('test_items.csv'))
