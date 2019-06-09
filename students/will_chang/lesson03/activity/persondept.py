"""
Creates functionality to add, search, delete, update, and list customers.
"""

from personjob_modeli import *

import logging
import peewee
from customer_model import Customer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Department class')

DEPT_NUM = 0
DEPT_NAME = 1
DEPT_MANAGER = 2
START = 3
END = 4
PERSON = 5

depts = [
    ('C305', 'Civil', 'Bob', '2017-07-15', '2019-05-20', 'Jim'),
    ('A202', 'Aero', 'Elon Musk', '2009-03-01', '2018-06-20', 'Pam'),
    ('H001', 'HR', 'Jeff Bezos', '2010-01-01', '2019-04-01', 'Dwight')
    ]

logger.info('Creating Department records: iterate through the list of tuples')
logger.info('Prepare to explain any errors with exceptions')
logger.info('and the transaction tells the database to rollback on error')

for dept in depts:
    try:
        with database.transaction():
            new_dept = Department.create(
                    dept_num = dept[DEPT_NUM],
                    dept_name = dept[DEPT_NAME],
                    dept_manager = dept[DEPT_MANAGER],
                    start_date = dept[START],
                    end_date = dept[END],
                    person_employed = dept[PERSON])
            new_dept.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NUM]}')
        logger.info(e)

logger.info('Read and print all Department records we created...')

for dept in Department:
    logger.info(f'{dept.dept_num} is the {dept.dept_name} department ' +\
        f'managed by {dept.dept_manager}. {dept.person_employed} worked ' +\
        f'here from {dept.start_date} to {dept.end_date}.')

database.close()
logger.info('Database closed')