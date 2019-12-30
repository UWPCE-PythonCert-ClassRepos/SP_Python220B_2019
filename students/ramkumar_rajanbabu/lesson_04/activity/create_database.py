"""Module for creating database"""

import logging
import customer_model as cm

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)  # Global variable

cm.DATABASE.create_tables([cm.Customer])
LOGGER.info("Created customers.db database in sqlite3")
cm.DATABASE.close()
