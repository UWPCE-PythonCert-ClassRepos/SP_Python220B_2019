"""
This file's sole purpose is to time the two different methods of importing data
"""

import logging
from timeit import timeit as timer
import linear
import parallel

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'method_timer.log'
FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE)
FILE_HANDLER.setLevel(logging.DEBUG)
FILE_HANDLER.setFormatter(FORMATTER)
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(logging.DEBUG)

if __name__ == "__main__":
    LOGGER.debug("Linear program time: %s seconds", timer(
        'linear.import_data()', globals=globals(), number=1))

    linear.delete_database()
    LOGGER.debug("Linear database cleared")

    LOGGER.debug("Parallel program time: %s seconds", timer(
        'parallel.import_data()', globals=globals(), number=1))

    parallel.delete_database()
    LOGGER.debug("Parallel database cleared")