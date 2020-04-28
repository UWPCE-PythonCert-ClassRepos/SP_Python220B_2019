'''
Basic opertions

'''

from customer_model import *
from peewee import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = SqliteDatabase('customers.db')




