"""
    Create database examle with Peewee ORM, sqlite and Python

"""
import logging
from personjob_model import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

database.create_tables([
        Job,
        Person,
        PersonNumKey
    ])

database.close()
