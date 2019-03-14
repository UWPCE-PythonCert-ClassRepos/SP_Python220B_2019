"""
    Creates the databases (tables) for lesson03 assignment.
"""
# pylint: disable=W0614, W0401, C0103, R0903
import logging
from customer_model import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Creates a database based on Customer model')
database.create_tables([Customer])
database.close()
