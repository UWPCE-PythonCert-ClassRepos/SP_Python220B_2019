#! /usr/bin/env python3

from peewee import *
from datetime import datetime
import logging

database = SqliteDatabase('employees.db')
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger('console')

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

class Department(BaseModel):
    """
        This class defines Department, which maintains a list of possible
        parts of the business in which a person my work
    """
    logger.info('Now to add the Department number a primary key')
    department_number = CharField(primary_key = True, max_length = 4)
    logger.info('Now add the Department name')
    department_name = CharField(max_length = 30)
    logger.info('Now add the foreign relationship of the manager')
    department_manager = ForeignKeyField(Person, to_field='person_name', null=True)

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

class PersonJobDepartment(BaseModel):
    person = ForeignKeyField(Person, to_field='person_name', null=False)
    job = ForeignKeyField(Job, to_field='job_name', null=False)
    department = ForeignKeyField(Department, to_field='department_number', null=False)
    duration_days = DecimalField(max_digits = 7, decimal_places = 0)


persons = [{'name':'Jon', 'town':'Vancouver', 'nickname':'Johnny'},
           {'name':'Joe', 'town':'Portland', 'nickname':None},
           {'name':'Mae', 'town':'Surrey', 'nickname':'Maybel'},
           {'name':'Sandoval', 'town':'Chiapis', 'nickname':'Sandy'},
           {'name':'Echo', 'town':'New York', 'nickname':'E'},
           {'name':'Gregor', 'town':'Smolensk', 'nickname':'Gregorii'}]

jobs = [{'title':'Vermin Wrangler', 'start':'2014-01-21', 'end':'2015-04-05', 'salary':300},
        {'title':'Magnetar', 'start':'2015-06-01', 'end':'2018-01-01', 'salary':3000},
        {'title':'Greg Pal', 'start':'2005-01-03', 'end':'2019-08-01', 'salary':3500},
        {'title':'Dog Catcher', 'start':'2003-01-30', 'end':'2018-04-03', 'salary':400},
        {'title':'Astronaut', 'start':'2001-01-03', 'end':'2020-01-05', 'salary':5000}]


departments = [{'department_number':'A015', 'department_name':'Animals', 'department_manager':'Jon'},
               {'department_number':'A016', 'department_name':'Physics', 'department_manager':'Mae'},
               {'department_number':'A017', 'department_name':'Friends', 'department_manager':'Sandoval'},
               {'department_number':'A018', 'department_name':'Space', 'department_manager':'Gregor'}]

relationships = [{'name':'Jon', 'title':'Vermin Wrangler', 'department':'A015'},
                 {'name':'Joe', 'title':'Magnetar', 'department':'A016'},
                 {'name':'Mae', 'title':'Astronaut', 'department':'A017'},
                 {'name':'Sandoval', 'title':'Greg Pal', 'department':'A018'},
                 {'name':'Echo', 'title':'Dog Catcher', 'department':'A015'},
                 {'name':'Gregor', 'title':'Astronaut', 'department':'A018'}]

def populate_people(persons):
    try:
        for person in persons:
            current = Person.get_or_create(person_name=person['name'], lives_in_town=person['town'], nickname=person['nickname'])
            logger.debug('Saved %s succeeded', current)
    except IntegrityError:
        logger.debug('Save failed.')

def populate_jobs(jobs):
    try:
        for job in jobs:
            current = Job.get_or_create(job_name=job['title'],
                                        start_date=job['start'],
                                        end_date=job['end'],
                                        salary=job['salary'])
            logger.debug('Saved %s succeeded', current)
    except IntegrityError:
        logger.debug('Save failed')

def populate_department(departments):
    try:
        for department in departments:
            current = Department.get_or_create(department_number=department['department_number'],
                                        department_name=department['department_name'],
                                        department_manager=department['department_manager'])
            logger.debug('Saved %s succeeded', current)
    except IntegrityError as error:
        logger.debug('Save of department failed %s', error)

def link_person_job_department(person, job, department, start_date, end_date):
    date_format = "%Y-%m-%d"
    try:
        duration = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
        current = PersonJobDepartment.get_or_create(person=person.person_name,
                                             job=job.job_name,
                                             department=department.department_number,
                                             duration_days=duration.days)
        logger.debug('Saved relationship %s', current)
    except IntegrityError as error:
        logger.debug('Unable to save relationship. %s', error)

def link_people_jobs_departments(relationships):
    try:
        for relationship in relationships:
            current_person = Person.get(Person.person_name == relationship['name'])
            current_job = Job.get(Job.job_name == relationship['title'])
            current_department = Department.get(Department.department_number == relationship['department'])

            link_person_job_department(current_person,
                                       current_job,
                                       current_department,
                                       current_job.start_date,
                                       current_job.end_date)
    except:
        logger.debug('Unexpected Error')

def output_report():
    for record in PersonJobDepartment.select():
        print("Employee: {:10} Job: {:20} Department: {:5} Duration: {:5}".format(str(record.person),
                                                                                   str(record.job),
                                                                                   str(record.department),
                                                                                   str(record.duration_days)))


if database.is_closed():
    logger.debug("Opening DB Connection")
    database.connect()

try:
    database.create_tables([Person, Job, Department, PersonJobDepartment])
    logger.debug('Database created')
except IntegrityError:
    logger.debug('Database exists')

populate_people(persons)
populate_jobs(jobs)
populate_department(departments)
link_people_jobs_departments(relationships)
output_report()

database.close()
