'''
inventory.py
'''
import csv
import os.path
import logging
import csv_handler as csvh

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_furniture(invoice_file, customer_name,
                  item_code, item_description,
                  item_monthly_cost):
    ''' write new items to the invoice file '''
    # if invoice file already exists
    if os.path.isfile(invoice_file):
        csvfile = open(invoice_file)
        csv_reader = csv.reader(csvfile, delimiter=',')

        for row in csv_reader:
            if customer_name in list(row):
                with open(invoice_file, 'a') as append_file:
                    logger.info(f'customer {customer_name} found in file')
                    append_file.write(f'{customer_name},{item_code},{item_description},{item_monthly_cost}\n')
                    break
        else:
            with open(invoice_file, 'a') as append_file:
                logger.info(f'customer {customer_name} not found in file')
                append_file.write(f'{customer_name},{item_code},{item_description},{item_monthly_cost}\n')

    # if invoice file is not found
    # create it and call add_furniture
    else:
        with open(invoice_file, 'w'):
            logger.info(f'Creating invoice file {invoice_file}')
            add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_cost)

def create_reader(csv_file):
    ''' creates csv reader object '''
    print(f"trying to find {csv_file}")
    if os.path.isfile(csv_file):
        try:
            return csv.reader(open(csv_file), delimiter=',')
        except FileNotFoundError as e:
            print(f'{e}')


def single_customer(customer_name, invoice_file):
    ''' outter function that takes a customer and csv file '''
    def invoice(rental_file):
        rental_reader = create_reader(rental_file)
        for row in rental_reader:
            add_furniture(invoice_file,customer_name,row[0],row[1],row[2])

    return invoice

create_invoice = single_customer("susan wong", "./lesson_8/data/invoice_file.csv")
create_invoice("./lesson_8/data/test_items.csv")
add_furniture('./lesson_8/data/invoice_file.csv', "Dan Wong", "prd001", "seat", 10.00)

