"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('personjobdept.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database

class Department(BaseModel):
    """ This class defines Department, which maintainns details of departments
    various jobs are in.
    """
    logger.info("Department class is used to identify the department a job was held in.")
    logger.info("department_number is the primary key")
    department_number = CharField(primary_key = True, max_length = 4)
    logger.info("Department has name and manager name fields")
    department_name = CharField(max_length = 30)
    department_manager_name = CharField(max_length = 30)

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    job_name = CharField(primary_key = True, max_length = 30)
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    person_employed = ForeignKeyField(Person, related_name= 'was_filled_by', null = False)
    logger.info("Adding a foreign key field to link to the new Department table key.")
    department = ForeignKeyField(Department, related_name= 'job_is_in', null = False)

class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)


