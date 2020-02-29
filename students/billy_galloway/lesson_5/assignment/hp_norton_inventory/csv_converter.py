import csv
import json
import logging
import os
os.chdir('..')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def csv_reader(csv_file):
    with open(csv_file) as csvfile:
        hpnorton_db_reader = csv.DictReader(csvfile, delimiter=',')
        documents = [documents for documents in hpnorton_db_reader]

        return documents

def customer_format(documents):
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

def product_format(documents):
    for document in documents:
        product = {
            'product_id': document['product_id'],
            'description': document['description'],
            'product_type': document['product_type'],
            'quantity_available': document['quantity_available']
        }

        yield product

def rentals_format(documents):
    for document in documents:
        rental = {
            'customer_id': document['customer_id'],
            'name': document['name'],
            'home_address': document['home_address'],
            'phone_number': document['phone_number'],
            'email_address': document['email_address']
        }

        yield rental