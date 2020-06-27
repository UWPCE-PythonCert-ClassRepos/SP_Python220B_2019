#!/usr/bin/env python

from db_model import *
import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


query = (Person
         .select(Person, Job)
         .join(Job, JOIN.INNER)
        )

logger.info('Jobs that people have had ::: View matching records from both tables')

for person in query:
    logger.info(f'Person {person.person_name} had job {person.job.job_name}')




query2 = (Department
         .select(Department, Job)
         .join(Job, JOIN.INNER)
         #.order_by(Department.dept_name)
        )

logger.info('Departments that people are in ::: View matching records from both tables')

for dept in query2:
    logger.info(f'\nJob of {dept.job.job_name} is in the {dept.dept_name} CODE: {dept.dept_code}')
    #logger.info(f'He lives in {dept.person.lives_in_town}, but the department is located in {dept.location}\n')

query3 = (Job
         .select(Job)
          )
        
logger.info('Logging time worked in a job\n\n\n')
#.select(Person, fn.COUNT(Job.job_name).alias('job_count'))
for job in query3:
    days = (datetime.datetime.strptime(job.end_date, '%Y-%m-%d') - datetime.datetime.strptime(job.start_date, '%Y-%m-%d')).days  
    #logger.info(f'Job is {job.job_name} between the dates of {job.start_date} - {job.end_date}')
    logger.info(f'{job.person_employed} was a {job.job_name} between {job.start_date} - {job.end_date}, a total of {days} days!')


