"""
Victor Medina
Purpose: Build the Customers class in the database""
"""

import logging

from customer_model_schema import *

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

database.create_tables([Customer])

database.close()
