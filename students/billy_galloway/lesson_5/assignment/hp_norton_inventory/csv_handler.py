import csv
import logging
import os
os.chdir('..')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CsvHandler():
    @staticmethod
    def csv_reader(csv_file):
        ''' ingests csv file and returns an ordered dict '''
        logger.info(f' Running csv reader')
        with open(csv_file) as csvfile:
            hpnorton_db_reader = csv.DictReader(csvfile, delimiter=',')
            logger.info(f'File {csv_file} Found')
    
            return [documents for documents in hpnorton_db_reader]

    @staticmethod
    def customer_format(documents):
        ''' formats customer data to dictionary '''
        for document in documents:
            customer = {
                'customer_id': document['customer_id'],
                'name': document['name'],
                'home_address': document['home_address'],
                'email_address': document['email_address'],
                'phone_number': document['phone_number'],
                'status': document['status'],
                'credit_limit': document['credit_limit']
            }

            yield customer

    @staticmethod
    def product_format(documents):
        ''' formats product data to dictionary '''
        for document in documents:
            product = {
                'product_id': document['product_id'],
                'description': document['description'],
                'product_type': document['product_type'],
                'quantity_available': document['quantity_available']
            }

            yield product

    @staticmethod
    def rentals_format(documents):
        ''' formats rentals data to dictionary '''
        for document in documents:
            rental = {
                'customer_id': document['customer_id'],
                'name': document['name'],
                'home_address': document['home_address'],
                'phone_number': document['phone_number'],
                'email_address': document['email_address']
            }

            yield rental

    @staticmethod
    def generate_document_list(*args):
        for i in args:
            documents = csv_reader(i)
            [document_type for document_type in customer_format(documents)]