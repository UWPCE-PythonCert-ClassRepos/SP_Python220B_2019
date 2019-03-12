"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)
"""

from personjob_modeli import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Department class')

logger.info('Creating Department records: just like Person. We use the foreign key')

DEPT_NUMBER = 0
DEPT_NAME = 1
DEPT_MANAGER = 2
START_DATE = 3
END_DATE = 4
PERSON = 5

depts = [
    ('A542', 'Sales', 'Jose', '2001-09-22', '2003-01-30', 'Andrew'),
    ('F998', 'Engineering', 'Juan', '2003-02-01', '2006-10-22', 'Andrew'),
    ('T123', 'Horses', 'Matt', '2006-10-23', '2016-12-24', 'Andrew'),
    ('B123', 'Walrus', 'John', '2012-10-01', '2014-11,10', 'Peter'),
    ('M554', 'Toliet', 'Xander', '2014-11-14', '2018-01-05', 'Peter')
    ]

for dept in depts:
    try:
        with database.transaction():
            new_dept = Department.create(
                d_number = dept[DEPT_NUMBER],
                d_name = dept[DEPT_NAME],
                d_manager = dept[DEPT_MANAGER],
                start_date = dept[START_DATE],
                end_date = dept[END_DATE],
                person_employed = dept[PERSON])
            new_dept.save()

    except Exception as e:
        logger.info(f'Error creating = {dept[DEPT_NUMBER]}')
        logger.info(e)

logger.info('Reading and print all department rows (note the value of person)...')

for dept in Department:
    logger.info(f'{dept.d_number} : {dept.start_date} to {dept.end_date} for {dept.person_employed}')
    logger.info(f'{dept.d_duration}')

database.close()
