'''
CSV Handler
'''
import csv
import logging
import os
from function_timer import timer
os.chdir('..')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CsvHandler():
    ''' csv handler class '''
    @staticmethod
    @timer
    def csv_reader(csv_file):
        ''' ingests csv file and returns an ordered dict '''
        logger.info(f' Running csv reader')
        return csv.reader(open(csv_file), delimiter=',')

    @staticmethod
    @timer
    def customer_format(documents):
        ''' formats customer data to dictionary '''
        for document in documents:
            customer = {
                'customer_id': document[0],
                'name': document[1],
                'home_address': document[2],
                'email_address': document[3],
                'phone_number': document[4],
                'status': document[5],
                'credit_limit': document[6]
            }

            yield customer

    @staticmethod
    @timer
    def product_format(documents):
        ''' formats product data to dictionary '''
        for document in documents:
            product = {
                'product_id': document[0],
                'description': document[1],
                'product_type': document[2],
                'quantity_available': document[3]
            }

            yield product

    @staticmethod
    @timer
    def rentals_format(documents):
        ''' formats rentals data to dictionary '''
        for document in documents:
            rental = {
                'product_id': document[0],
                'customer_id': document[1],
                'name': document[2],
                'home_address': document[3],
                'phone_number': document[4],
                'email_address': document[5]
            }

            yield rental

    @timer
    def generate_document_list(self, document, item_key):
        '''
            takes a csv file along with the inventory type i.e. customer, product, rentals
            as an argument and passes it to the csv_reader. That gets passed as an
            argument to the formatter to be returned as a list of dictionaries
        '''
        item_type = {
            'customer': self.customer_format,
            'product': self.product_format,
            'rental': self.rentals_format
        }

        documents = self.csv_reader(document)

        return [inventory_type for inventory_type in item_type[item_key](documents)]
