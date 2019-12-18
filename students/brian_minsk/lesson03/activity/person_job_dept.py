"""
    BSM - I just copied the code from personjob_learning_v3_p1.py and 
    personjob_learning_v5_p1.py to add Person and Job data to the database.
    I then added my own code to add Department data to the  database.
"""

from personjob_modeli import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with Person class')
logger.info('Note how I use constants and a list of tuples as a simple schema')
logger.info('Normally you probably will have prompted for this from a user')

PERSON_NAME = 0
LIVES_IN_TOWN = 1
NICKNAME = 2

people = [
    ('Andrew', 'Sumner', 'Andy'),
    ('Peter', 'Seattle', None),
    ('Susan', 'Boston', 'Beannie'),
    ('Pam', 'Coventry', 'PJ'),
    ('Steven', 'Colchester', None),
    ]

# logger.info('Creating Person records: iterate through the list of tuples')
# logger.info('Prepare to explain any errors with exceptions')
# logger.info('and the transaction tells the database to rollback on error')

logger.info('Populating the Person table with data.')
for person in people:
    try:
        with database.transaction():
            new_person = Person.create(
                    person_name = person[PERSON_NAME],
                    lives_in_town = person[LIVES_IN_TOWN],
                    nickname = person[NICKNAME])
            new_person.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

# logger.info('Read and print all Person records we created...')

# for person in Person:
#     logger.info(f'{person.person_name} lives in {person.lives_in_town} ' +\
#         f'and likes to be known as {person.nickname}')

# database.close()
DEPT_NUMBER = 0
DEPT_NAME = 1
DEPT_MANAGER = 2

departments = [('MSW1', 'Ministry of Silly Walks', 'John Cleese'),
               ('MBS1', 'Ministry of Boring Stuff', 'Bobble Wobble'),
               ('MNS1', 'Ministry of Nihilistic Studies', 'Friedrich Nietzsche')]

logger.info("Populating the Department table with data.")

for department in departments:
    try:
        with database.transaction():
            new_department = Department.create(
                department_number = department[DEPT_NUMBER],
                department_name = department[DEPT_NAME],
                department_manager_name = department[DEPT_MANAGER])
            new_department.save()

    except Exception as e:
        logger.info(f'Error creating = {department[DEPT_NUMBER]}')
        logger.info(e)

JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4
DEPARTMENT = 5

logger.info("Adding data for the department_number foreign key field.")
jobs = [
    ('Analyst', '2001-09-22', '2003-01-30',65500, 'Andrew', 'MSW1'),
    ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'MSW1'),
    ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'MBS1'),
    ('Admin supervisor', '2012-10-01', '2014-11,10', 45900, 'Peter', 'MSW1'),
    ('Admin manager', '2014-11-14', '2018-01,05', 45900, 'Peter', 'MNS1')
    ]

logger.info('Populating the Job table with data.')
for job in jobs:
    try:
        with database.transaction():
            new_job = Job.create(
                job_name = job[JOB_NAME],
                start_date = job[START_DATE],
                end_date = job[END_DATE],
                salary = job[SALARY],
                person_employed = job[PERSON_EMPLOYED],
                department = job[DEPARTMENT])
            new_job.save()

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

# logger.info('Reading and print all Job rows (note the value of person)...')

# for job in Job:
#     logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')



database.close()
