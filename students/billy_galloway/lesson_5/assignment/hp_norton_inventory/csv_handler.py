'''
CSV Handler
'''
import csv
import logging
import os
os.chdir('..')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CsvHandler():
    ''' csv handler class '''
    @staticmethod
    def csv_reader(csv_file):
        ''' ingests csv file and returns an ordered dict '''
        logger.info(f' Running csv reader')
        with open(csv_file) as csvfile:
            hpnorton_db_reader = csv.DictReader(csvfile, delimiter=',')
            logger.info(f' File {csv_file} Found')

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
                'product_id': document['product_id'],
                'customer_id': document['customer_id'],
                'name': document['name'],
                'home_address': document['home_address'],
                'phone_number': document['phone_number'],
                'email_address': document['email_address']
            }

            yield rental

    def generate_document_list(self, document, item_key):
        '''
            takes a csv file along with the inventory type i.e. customer, product, rentals
            as an argument and passes it to the csv_reader. That gets passed as an
            argument to the formatter to be returned as a list of dictionaries
        '''
        item_type = {
            'customer': self.customer_format,
            'product': self.product_format,
            'rentals': self.rentals_format
        }

        documents = self.csv_reader(document)
        logger.info(f' Yield documents for formatting')

        return [inventory_type for inventory_type in item_type[item_key](documents)]
