"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)

    Department:
        1. insert records
        2. display all records
        3. show transactions
        4. show error checking
        5. show logging (to explain what's going on)

"""

from personjob_modeli import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Department class')

DEPARTMENT_NUMBER = 0
DEPARTMENT_NAME = 1
MANAGER_NAME = 2

org = [
    ('1', 'Human Resources', 'Julie'),
    ('2', 'Finance', 'Mary'),
    ('3', 'Sales', 'Rick'),
    ]

logger.info('Creating Department records: iterate through the list of tuples')
logger.info('Prepare to explain any errors with exceptions')
logger.info('and the transaction tells the database to rollback on error')

for department in org:
    try:
        with database.transaction():
            new_department = Department.create(
                    department_number = department[DEPARTMENT_NUMBER],
                    department_name = department[DEPARTMENT_NAME],
                    manager_name = department[MANAGER_NAME])
            new_department.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

logger.info('Read and print all Department records we created...')

for department in Department:
    logger.info(f'{department.department_name} reports to {department.manager_name} ' +\
        f'and has the code of {department.department_number}')

database.close()
