'''
This module is used to practice working with Sqlite and Peewee.
'''

from personjob_model import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Now we need to track in which Department a Person held a Job.")

NAME = 0
CITY = 1
NICKNAME = 2

people = [
    ('Peter', 'Seattle', 'Pete'),
    ('Alexander', 'Dallas', 'Alex'),
    ('Robert', 'Austin', 'Rob')
]

for person in people:
    try:
        with database.transaction():
            new_person = Person.create(
                person_name = person[NAME],
                lives_in_town = person[CITY],
                nickname = person[NICKNAME]
            )
            new_person.save()
            logger.info('Saved new person to DB')

    except Exception as e:
        logger.info('Error while trying to save new person to DB') # not caught; no error thrown by Peewee
        logger.info(e)


DEPT_NUM = 0
DEPT_NAME = 1
DEPT_MGR = 2

depts = [
    ('0001', 'Computer Science', 'Peter'),
    ('0002', 'Mechanical Engineering', 'Alexander'),
    ('0003', 'Computer Engineering', 'Robert')
]

for dept in depts:
    try:
        with database.transaction():
            new_dept = Department.create(
                dept_num = dept[DEPT_NUM],
                dept_name = dept[DEPT_NAME],
                dept_manager = dept[DEPT_MGR]
            )
            new_dept.save()
            logger.info('Saved new department to DB')

    except Exception as e:
        logger.info('Error while trying to save new dept to DB') # not caught; no error thrown by Peewee
        logger.info(e)

loaded_people = Person.select()
loaded_depts = Department.select()

for loaded_person in loaded_people:
    print(f'Person name: {loaded_person.person_name}')
    print(f'Lives in town: {loaded_person.lives_in_town}')
    print(f'Nickname: {loaded_person.nickname}')

for loaded_dept in loaded_depts:
    print(f'Department number: {loaded_dept.dept_num}')
    print(f'Department name: {loaded_dept.dept_name}')
    print(f'Department manager: {loaded_dept.dept_manager}')