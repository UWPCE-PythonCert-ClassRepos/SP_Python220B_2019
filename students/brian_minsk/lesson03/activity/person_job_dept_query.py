"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)


"""

from personjob_modeli import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Job class')

logger.info('Now resolve the join and print (INNER shows only jobs that match person)...')
logger.info('Notice how we use a query variable in this case')
logger.info('We select the classes we need, and we join Person to Job')
logger.info('Inner join (which is the default) shows only records that match')

query = (Job
         .select(Person.person_name, Job.job_name, Department.department_name)
         .join(Person)
         .switch(Job)
         .join(Department)
        )

logger.info('View matching records from both tables')

for job in query:
    logger.info(f'Person {job.person_employed.person_name} had job {job.job_name} in the {job.department.department_name}')


database.close()
