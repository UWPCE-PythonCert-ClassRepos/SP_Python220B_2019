"""Module to initialize a database from the customer_model schema file"""

from customer_model import *

database.create_tables([Customer])

database.close()
