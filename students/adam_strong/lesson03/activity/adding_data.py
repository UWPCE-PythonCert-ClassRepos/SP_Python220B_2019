#!/usr/bin/env python

"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)


"""

from db_model import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
logger.info('Filling in Department table')

DEPART = 0
DEPART_CODE = 1
DEP_MANAGER = 2

departments = [
    ('Research and Development', 'RD01', 'Zippy'),
    ('Sales', 'S103', 'Gordon'),
    ('Manufacturing', 'MN45', 'Steelsy'),
    ('Marketing', 'MAR1', 'Andrew')
    ]

for dept in departments:
    try:
        with database.transaction():
            new_dept = Department.create(
                    dept_name = dept[DEPART],
                    dept_code = dept[DEPART_CODE],
                    manager = dept[DEP_MANAGER])

    except Exception as e:
        logger.info(f'Error creating = {departments[DEPART]}')
        logger.info(e)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
logger.info('Filling in Person table')

PERSON_NAME = 0
LIVES_IN_TOWN = 1
NICKNAME = 2

people = [
    ('Andrew', 'Tacoma', 'Andy'),
    ('Peter', 'Pittsburg', None),
    ('Susan', 'Eugene', 'Beannie'),
    ('Pam', 'Coventry', 'PJ'),
    ('Steven', 'Colchester', None),
    ('Zippy', 'Seattle', 'Zips'),
    ('Gordon', 'Philidalphea', 'Gecko'),
    ('Steelsy', 'Eugene', None)
    ]

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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`
logger.info('Filling in Job table')

JOB_NAME = 0
START_DATE = 1
END_DATE = 2
SALARY = 3
PERSON_EMPLOYED = 4
JOB_DEPT = 5

jobs = [
    ('Analyst', '2001-09-22', '2003-01-30', 65500, 'Andrew', 'RD01'),
    ('Senior analyst', '2003-02-01', '2006-10-22', 70000, 'Andrew', 'RD01'),
    ('Senior business analyst', '2006-10-23', '2016-12-24', 80000, 'Andrew', 'MAR1'),
    ('Sales supervisor', '2012-10-01', '2014-11-10', 45900, 'Peter', 'S103'),
    ('Sales manager', '2014-11-14', '2018-01-05', 45900, 'Peter', 'S103')
    ]


for job in jobs:
    try:
        with database.transaction():
            new_job = Job.create(
                job_name = job[JOB_NAME],
                start_date = job[START_DATE],
                end_date = job[END_DATE],
                salary = job[SALARY],
                person_employed = job[PERSON_EMPLOYED],
                dept_code = job[JOB_DEPT])
            new_job.save()

    except Exception as e:
        logger.info(f'Error creating = {job[JOB_NAME]}')
        logger.info(e)

logger.info('Reading and print all rows (note the value of person)...')

logger.info('\nRecords in the Department Table:\n')
for dept in Department:
    logger.info(f'{dept.dept_name} with code {dept.dept_code} run by {dept.manager}')

logger.info('\nRecords in the Person Table:\n')
for member in Person:
    logger.info(f'{member.person_name} lives in the {member.lives_in_town}')

logger.info('\nRecords in the Job Table:\n')
for job in Job:
    logger.info(f'{job.job_name} : {job.start_date} to {job.end_date} for {job.person_employed}')


database.close()
