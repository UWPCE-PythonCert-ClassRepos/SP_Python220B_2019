"""setup file"""
# pylint: disable=unused-import, unused-wildcard-import,
# pylint: disable=too-few-public-methods, too-many-arguments, wildcard-import
# pylint: disable=logging-format-interpolation, pointless-string-statement
from peewee import *
from customers import *

DATABASE = SqliteDatabase('customers.db')
DATABASE.connect()
DATABASE.execute_sql('PRAGMA foreign_keys = ON;')

with DATABASE:
    DATABASE.create_tables([Customer])
