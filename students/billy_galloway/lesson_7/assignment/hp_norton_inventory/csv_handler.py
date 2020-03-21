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
        csvfile = open(csv_file)
        hpnorton_db_reader = csv.reader(csvfile, delimiter=',')
        logger.info(f' File {csv_file} Found')

        return hpnorton_db_reader

    @staticmethod
    def customer_format(documents):
        ''' formats customer data to dictionary '''
        logger.info(f'Received {documents} starting format')
        for document in documents:
            ldocument = list(document)
            customers = {
                'customer_id': ldocument[0],
                'name': ldocument[1],
                'home_address': ldocument[2],
                'email_address': ldocument[3],
                'phone_number': ldocument[4],
                'status': ldocument[5],
                'credit_limit': ldocument[6]
            }

            yield customers

    @staticmethod
    def product_format(documents):
        ''' formats product data to dictionary '''
        logger.info(f'Received {documents} starting format')
        for document in documents:
            ldocument = list(document)
            products = {
                'product_id': ldocument[0],
                'description': ldocument[1],
                'product_type': ldocument[2],
                'quantity_available': ldocument[3]
            }

            yield products

    @staticmethod
    def rentals_format(documents):
        ''' formats rentals data to dictionary '''
        for document in documents:
            ldocument = list(document)
            rentals = {
                'product_id': ldocument[0],
                'customer_id': ldocument[1],
                'name': ldocument[2],
                'home_address': ldocument[3],
                'phone_number': ldocument[5],
                'email_address': ldocument[4]
            }

            yield rentals

    def generate_document_list(self, document, item_key, document_queue):
        '''
            takes a csv file along with the inventory type i.e. customer, product, rentals
            as an argument and passes it to the csv_reader. That gets passed as an
            argument to the formatter to be returned as a list of dictionaries
        '''
        item_type = {
            'product': self.product_format,
            'customer': self.customer_format,
            'rental': self.rentals_format
        }

        documents = self.csv_reader(document)
        logger.info(f' Yield documents for formatting')

        document_queue.put(item_type[item_key](documents))
