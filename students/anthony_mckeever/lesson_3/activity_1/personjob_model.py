# Advanced Programming In Python - Lesson 3 Activity 1: Relational Databases
# RedMine Issue - SchoolOps-13
# Code Poet: Anthony McKeever
# Start Date: 10/30/2019
# End Date: 10/31/2019

"""
Simple database example with Peewee ORM, sqlite and Python
Here we define the schema
Use logging for messages so they can be turned off
"""

import sys
import logging
from datetime import datetime

from peewee import SqliteDatabase
from peewee import IntegrityError
from peewee import Model

from peewee import CharField
from peewee import DateField
from peewee import DecimalField
from peewee import ForeignKeyField

# pylint: disable=too-few-public-methods

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

LOGGER.info('Naming and connecting to database...')

DATABASE = SqliteDatabase('personjob.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

LOGGER.info('Defining data schema...')


class BaseModel(Model):
    """ The Base Model """
    class Meta:
        """ The Meta class """
        database = DATABASE


class Person(BaseModel):
    """
    This class defines Person, which maintains details of someone
    for whom we want to research career to date.
    """
    LOGGER.info('Define Person table...')

    person_name = CharField(primary_key=True, max_length=30)
    lives_in_town = CharField(max_length=40)
    nickname = CharField(max_length=20, null=True)

    LOGGER.info("Table defined successfully.")


class Job(BaseModel):
    """
    This class defines Job, which maintains details of past JOBS
    held by a Person.
    """
    LOGGER.info('Define Job table...')

    job_id = CharField(primary_key=True, max_length=4)
    job_name = CharField(max_length=30)

    LOGGER.info("Table defined successfully.")


class PersonToJob(BaseModel):
    """ Maps a person to a job. """
    LOGGER.info('Define PersonToJob table...')

    person_name = ForeignKeyField(Person, to_field="person_name")
    job_id = ForeignKeyField(Job, to_field="job_id")

    start_date = DateField(formats='YYYY-MM-DD')
    end_date = DateField(formats='YYYY-MM-DD')

    salary = DecimalField(max_digits=7, decimal_places=2)
    duration_days = DecimalField(max_digits=7, decimal_places=0, null=True)

    LOGGER.info("Table defined successfully.")


class Department(BaseModel):
    """
    This class defines Department
    """
    LOGGER.info('Define Department table...')

    department_name = CharField(max_length=30)
    department_id = CharField(primary_key=True, max_length=4)
    manager = ForeignKeyField(Person, to_field='person_name', null=True)

    LOGGER.info("Table defined successfully.")


class PersonToDepartment(BaseModel):
    """ Maps a person to a department. """
    LOGGER.info('Define PersonToDepartment table...')

    person = ForeignKeyField(Person, to_field="person_name", null=False)
    department = ForeignKeyField(Department,
                                 to_field="department_id",
                                 null=False)

    LOGGER.info("Table defined successfully.")


PEOPLE = [{"name": "Kima", "town": "Yukayosha", "nickname": None},
          {"name": "Delilah", "town": "Misty Autumn", "nickname": "Lilah"},
          {"name": "Astra", "town": "Almia", "nickname": None},
          {"name": "Cresenta", "town": "Almia", "nickname": "Cressy"},
          {"name": "Katie", "town": "Lovel", "nickname": "Kate"},
          {"name": "Mayrina", "town": "Collette", "nickname": "Mari"},
          {"name": "Kayomi", "town": "New Sophiesville", "nickname": "Yomi"},
          {"name": "Svetlana", "town": "Kiev", "nickname": "Lana"},
          {"name": "Phoebe", "town": "Ekiya Space Station", "nickname": None}]

JOBS = [{"title": "Temporal Analyst I", "id": "TA01"},
        {"title": "Temporal Developer I", "id": "TD01"},
        {"title": "Temporal Facilitator I", "id": "TF01"},
        {"title": "Deep Field Operative", "id": "DFO1"},
        {"title": "Near Field Operative", "id": "NFO1"},
        {"title": "Temporal Debugger", "id": "TDBR"},
        {"title": "Researcher III", "id": "RES3"}]

PEOPLE_JOBS = [{"name": "Kima", "job": "TF01",
                "start": "2323-04-13", "end": "2353-05-30", "salary": "7000"},
               {"name": "Delilah", "job": "TD01",
                "start": "2150-10-04", "end": "2353-05-30", "salary": "7000"},
               {"name": "Astra", "job": "TA01",
                "start": "0012-06-19", "end": "2353-05-30", "salary": "7500"},
               {"name": "Cresenta", "job": "DFO1",
                "start": "2153-08-23", "end": "2153-09-08", "salary": "8231"},
               {"name": "Katie", "job": "TDBR",
                "start": "2170-12-26", "end": "2353-05-30", "salary": "6500"},
               {"name": "Mayrina", "job": "NFO1",
                "start": "2130-03-13", "end": "2167-02-14", "salary": "5000"},
               {"name": "Kayomi", "job": "NFO1",
                "start": "2103-11-01", "end": "2117-04-05", "salary": "5000"},
               {"name": "Svetlana", "job": "TDBR",
                "start": "1961-05-23", "end": "2353-05-30", "salary": "6000"},
               {"name": "Phoebe", "job": "RES3",
                "start": "2149-01-20", "end": "2154-01-19", "salary": "4600"}]

DEPTS = [{"name": "Temporal Integrity", "number": "T832", "manager": "Kima"},
         {"name": "Astrometic Intelligence",
          "number": "A149", "manager": "Mayrina"},
         {"name": "Temporal Refactory", "number": "T956", "manager": "Katie"},
         {"name": "Forbidden Weaponry", "number": "S004", "manager": "Phoebe"}]

RELATIONS = [{"name": "Kima", "department": "T832"},
             {"name": "Astra", "department": "T832"},
             {"name": "Delilah", "department": "T832"},
             {"name": "Cresenta", "department": "A149"},
             {"name": "Mayrina", "department": "A149"},
             {"name": "Kayomi", "department": "A149"},
             {"name": "Phoebe", "department": "S004"},
             {"name": "Katie", "department": "T956"},
             {"name": "Svetlana", "department": "T956"}]


def populate_people(list_people):
    """
    Populates people in the database

    :list_people:   The list of people to populate
    """
    LOGGER.info("Start populating people")

    for person in list_people:
        try:
            current = Person.get_or_create(person_name=person["name"],
                                           lives_in_town=person["town"],
                                           nickname=person["nickname"])
            LOGGER.debug('Saved Person: %s', current)
        except IntegrityError as integrity:
            LOGGER.debug("Failed to save person: %d", person)
            LOGGER.error(integrity)

    LOGGER.info("Finished populating people")


def populate_jobs(list_jobs):
    """
    Populates jobs in the database

    :list_jobs:   The list of jobs to populate
    """
    LOGGER.info("Start populating jobs")

    for job in list_jobs:
        try:
            current = Job.get_or_create(job_id=job["id"],
                                        job_name=job["title"])
            LOGGER.debug('Saved Job: %s', current)
        except IntegrityError as integrity:
            LOGGER.debug("Failed to save job: %d", job)
            LOGGER.error(integrity)

    LOGGER.info("Finished populating jobs")


def populate_person_to_job(list_people_job):
    """
    Populates people to jobs in the database

    :list_jobs:   The list of people to jobs to populate
    """
    LOGGER.info("Start populating PersonToJob")

    for people_job in list_people_job:
        try:
            duration = None
            start = people_job.get("start")
            end = people_job.get("end")

            if start is not None and end is not None:
                formatter = "%Y-%m-%d"
                start_date = datetime.strptime(start, formatter)
                end_date = datetime.strptime(end, formatter)
                duration = (end_date - start_date).days

            person = Person.get(Person.person_name == people_job["name"])
            job = Job.get(Job.job_id == people_job["job"])

            current = PersonToJob.get_or_create(person_name=person.person_name,
                                                job_id=job.job_id,
                                                start_date=start,
                                                end_date=end,
                                                salary=people_job["salary"],
                                                duration_days=duration)

            LOGGER.debug('Saved PersonToJob: %s', current)
        except IntegrityError as integrity:
            LOGGER.debug("Failed to save PersonToJob: %d", people_job)
            LOGGER.error(integrity)

    LOGGER.info("Finished populating PersonToJob")


def populate_departments(list_depts):
    """
    Populates departments in the database

    :list_depts:   The list of jobs to populate
    """
    LOGGER.info("Start populating departments")

    for dept in list_depts:
        try:
            current = Department.get_or_create(department_name=dept["name"],
                                               department_id=dept["number"],
                                               manager=dept["manager"])
            LOGGER.debug('Saved Department: %s', current)
        except IntegrityError as integrity:
            LOGGER.debug("Failed to save Department: %d", dept)
            LOGGER.error(integrity)

    LOGGER.info("Finished populating departments")


def populate_relations(list_relation):
    """
    Populates relations in the database

    :list_relation:   The list of relations to populate
    """
    LOGGER.info("Start populating PEOPLEToDepartment")
    for relation in list_relation:
        person = Person.get(Person.person_name == relation["name"])
        dept = Department.get(Department.department_id ==
                              relation["department"])

        PersonToDepartment.get_or_create(person=person.person_name,
                                         department=dept.department_id)

    LOGGER.info("Finished populating PEOPLEToDepartment")


def main():
    """
    The main method of the application.
    """
    try:
        LOGGER.info("Initialize database...")
        DATABASE.create_tables([Person, Job, PersonToJob,
                                Department, PersonToDepartment])
        LOGGER.info("Database initialized successfully.")

    except IntegrityError as integrity:
        LOGGER.error(integrity)
        LOGGER.info("Failed to initialize database.  Exiting.")

        sys.exit()

    populate_people(PEOPLE)
    populate_jobs(JOBS)
    populate_person_to_job(PEOPLE_JOBS)
    populate_departments(DEPTS)
    populate_relations(RELATIONS)


if __name__ == "__main__":
    main()
