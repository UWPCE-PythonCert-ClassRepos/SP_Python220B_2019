"""
    Learning persistence with Peewee and sqlite
    delete the database to start over
        (but running this program does not require it)


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

logger.info('Creating Person records, but in a new table with generated PK...')

for person in people:
    try:
        with database.transaction():
            new_person = PersonNumKey.create(
                    person_name = person[PERSON_NAME],
                    lives_in_town = person[LIVES_IN_TOWN],
                    nickname = person[NICKNAME])
            new_person.save()

    except Exception as e:
        logger.info(f'Error creating = {person[0]}')
        logger.info(e)

database.close()
