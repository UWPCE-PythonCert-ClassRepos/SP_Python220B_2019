from customer_model import *
import logging

customer_db.create_tables([Customer])

customer_db.close()
