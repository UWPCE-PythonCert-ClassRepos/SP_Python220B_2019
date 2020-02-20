from personjob_modeli import *

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Working with department class')
logger.info('Note how I use constants and a list of tuples as a simple schema')
logger.info('Normally you probably will have prompted for this from a user')

PERSON_NAME = 0
DEPT_NUM = 1
DEPT_NAME = 2
DEPT_MGR = 3
START_DATE = 4
END_DATE = 5

departments = [
    ('Andrew', 'A500', 'Accounting', 'Bob', '2018-01-01', '2019-08-08'),
    ('Susan', 'B100', 'IT','Ben','2018-02-01', '2019-09-09'),
    ('Pam', 'C200', 'Marketing', 'Paul', '2018-03-01', '2019-10-10')
    ]
query = (Person
         .select(Person, Department)
         .join(Department, JOIN.INNER)
        )

for person in departments:
    try:
        with database.transaction():
            dept_db = Department.create(
                    department_number = person[DEPT_NUM],
                    department_name = person[DEPT_NAME],
                    manager_name = person[DEPT_MGR])
            dept_db.save()
            logger.info('Database add successful')

    except Exception as e:
        logger.info(f'Error creating = {person[PERSON_NAME]}')
        logger.info(e)
        logger.info('See how the database protects our data')

logger.info('Read and print all department records we created...')

for department in Department:
    logger.info(f'{department.person_name} department: {department.department_name} ' +\
        f'department number: {department.department_number} manager: {department.manager_name} ' +\
        f'employeed: {department.start_date}')

database.close()