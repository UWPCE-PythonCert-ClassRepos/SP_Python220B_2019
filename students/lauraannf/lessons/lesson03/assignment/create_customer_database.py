# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:17:54 2019

@author: Laura.Fiorentino
"""

import logging
from customer_model import *

logging.basicConfig(level=logging.WARNING)
LOGGER = logging.getLogger(__name__)

DATABASE = SqliteDatabase('customers.db')

CUSTOMERS = [
    ('00001', 'Dorothy', 'Zbornak', 'Miami', '5551234567',
     'd.zbornak@gmail.com', True, 1000),
    ('00002', 'Sophia', 'Petrillo', 'Miami', '5551234568',
     's.petrillo@gmail.com', True, 1000),
    ('00003', 'Blanche', 'Devereaux', 'Miami', '5551234569',
     'b.devereaux@gmail.com', True, 5000),
    ('00004', 'Rose', 'Nylund', 'Miami', '5551234570',
     'r.nylund@gmail.com', True, 2000),
    ('00005', 'Stan', 'Zbornak', 'Hawaii', '5551234571',
     's.zbornak@gmail.com', False, 100),
    ]

for customer in CUSTOMERS:
    try:
        with DATABASE.transaction():
            new_customer = Customer.create(customer_ID=customer[0],
                                           first_name=customer[1],
                                           last_name=customer[2],
                                           home_address=customer[3],
                                           phone_number=customer[4],
                                           email_address=customer[5],
                                           status=customer[6],
                                           credit_limit=customer[7])
            new_customer.save()
    except Exception as ex:
        LOGGER.warning('Error creating %s', customer[1])
        LOGGER.warning(ex)
