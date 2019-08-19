#!/usr/bin/env python3

# Russell Felts
# Assignment 4 - Unit Tests

""" Creates the Customer Table in the Customer DB """

import logging
from customer_model import DATABASE, Customer

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info("Create the Customer Table.")
DATABASE.create_tables([Customer])
LOGGER.info("Closing the database")
DATABASE.close()
