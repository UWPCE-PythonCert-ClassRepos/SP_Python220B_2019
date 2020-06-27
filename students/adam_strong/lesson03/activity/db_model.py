#!/usr/bin/env python

"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off

"""
import logging
import datetime
from peewee import *

database = SqliteDatabase('personjob.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

class BaseModel(Model):
    class Meta:
        database = database


class Department(BaseModel):
    """
        This class defines Department, which maintains details of which 
        group any number of people (Person) belong to. 
    """   
    dept_name = CharField(max_length = 30)
    dept_code = CharField(primary_key = True, max_length = 4) # Starts with a letter and is always 4 digits long
    manager = CharField(max_length = 30)



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
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    dept_code = ForeignKeyField(Department, related_name='dept_codes', null = False)

'''
    @hybrid_property
    def total_days_worked(self):
        return (end_date - start_date).days


                rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
                logging.debug('Real start date value')

            #Checking that rental end has a value
            if value['rental_end'] == '':
                errcount += 1
                logging.warning('No end date')
            else:
                rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
                logging.debug('Real end date value')

            #If the dates are real, check that end date follows the start date
            if errcount == 0:
                value['total_days'] = (rental_end - rental_start).days
'''