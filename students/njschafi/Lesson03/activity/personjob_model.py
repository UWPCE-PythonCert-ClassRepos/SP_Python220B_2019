"""
    Simple database example with Peewee ORM, sqlite and Python
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

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

# if you wanted to use heroku postgres:
#
# psycopg2
#
# parse.uses_netloc.append("postgres")
# url = parse.urlparse(os.environ["DATABASE_URL"])
#
# conn = psycopg2.connect(
# database=url.path[1:],
# user=url.username,
# password=url.password,
# host=url.hostname,
# port=url.port
# )
# database = conn.cursor()
#
# Also consider elephantsql.com (be sure to use configparser for PWß)

logger.info('This means we can easily switch to a different database')

logger.info('Enable the Peewee magic! This base class does it all')

class BaseModel(Model):
    class Meta:
        database = database

logger.info('By inheritance only we keep our model (almost) technology neutral')

class Person(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')
    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """
    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key = True, max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.info('Number')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)

class PersonNumKey(BaseModel):
    """
        This class defines Person, which maintains details of someone
        for whom we want to research career to date.
    """
    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")
    person_name = CharField(max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

#For a Department, we need to know it’s department number,
#which is 4 characters long and starts with a letter.
#We need to know the department name (30 characters),
#and the name of the department manager (30 characters).
#We also need to know the duration in days that the job was held.
#Think about this last one carefully.
# ADDED BELOW FOR LESSON03 ACTIVITY
class Department(BaseModel):
    """
        This class defines the department, which maintains details of the
        department number, name, manager and duration the job was held.
    """
    logger.info('Now using the Department class') # TODO: Needs to start with a letter
    d_number = CharField(primary_key = True, max_length = 4)
    logger.info('Department Name')
    d_name = CharField(max_length = 30)
    logger.info('Department Manager')
    d_manager = CharField(max_length = 30)
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    logger.info('Duration')
    d_duration = (end_date - start_date)# TODO: May need to change this
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False) # TODO: Need to link
