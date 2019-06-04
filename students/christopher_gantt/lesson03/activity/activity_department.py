'''Experimenting with using the database, with the department class'''

from personjob_modeli import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

logger.info('Working with Department class')

DEPARTMENT_NUMBER = 0
DEPARTMENT_NAME = 1
DEPARTMENT_MANAGER = 2
JOB_TITLE = 3

departments = [
    ('D123', 'Business Analytics', 'Joseph', 'Business manager'),
    ('A456', 'Administration', 'Peter', 'Admin manager')]


