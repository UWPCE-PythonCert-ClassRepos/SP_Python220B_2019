"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)

    Department:
        1. insert records
        2. display all records
        3. show error checking
        4. show logging (to explain what's going on)

"""

from personjob_modeli import *
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Department class')
logger.info('Note how I use constants and a list of tuples as a simple schema')
logger.info('Normally you probably will have prompted for this from a user')

DEPARTMENT_NUMBER = 0
DEPARTMENT_NAME = 1
DEPARTMENT_MANAGER = 2
JOB = 3

departments = [
    ('A001', 'Admin', 'Michael Scott', 'Admin supervisor'),
    ('A002', 'Admin', 'Jan Levinson', 'Admin manager'),
    ('A003', 'IT', 'Darryl Philbin', 'Analyst'),
    ('A004', 'IT', 'Darryl Philbin', 'Senior analyst'),
    ('A005', 'Business Intelligence', 'Bob Vance', 'Senior business analyst')
    ]

logger.info('Creating Department records: iterate through the list of tuples')
logger.info('Prepare to explain any errors with exceptions')
logger.info('and the transaction tells the database to rollback on error')

for department in departments:
    try:
        with database.transaction():
            logger.info('Get job entry from database to access start and end dates')
            job_entry = Job.get(Job.job_name == department[JOB])
            start_date = datetime.strptime(job_entry.start_date,'%Y-%m-%d')
            end_date = datetime.strptime(job_entry.end_date,'%Y-%m-%d')
            logger.info(f'For job {job_entry.job_name}, start date = {start_date}, ' +\
                f'end date = {end_date}')
            logger.info('Take delta and convert to days')
            delta = (end_date - start_date).days
            new_department = Department.create(
                    dep_number = department[DEPARTMENT_NUMBER],
                    dep_name = department[DEPARTMENT_NAME],
                    dep_manager = department[DEPARTMENT_MANAGER],
                    job = department[JOB],
                    duration = delta)
            new_department.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {department[DEPARTMENT_NUMBER]}')
        logger.info(e)
        logger.info('See how the database protects our data')

logger.info('Read and print all Department records we created...')

for department in Department:
    logger.info(f'Number = {department.dep_number}, Name = {department.dep_name}, ' +\
        f'Manager = {department.dep_manager}, Job = {department.job}, ' +\
        f'Duration = {department.duration} days')

database.close()
