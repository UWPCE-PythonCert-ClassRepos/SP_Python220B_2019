#!/usr/bin/env python

"""
    Create database for HP Norton customers with Peewee ORM, sqlite and Python

"""
import logging
from customer_model import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Building the customer table')

database.create_tables([
        Customers])

database.close()
