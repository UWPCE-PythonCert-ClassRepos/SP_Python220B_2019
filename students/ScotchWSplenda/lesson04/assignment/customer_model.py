# pylint: disable=C0103,C0111,R0903
'''
Peewee ORM, sqlite and Python
what is this 'peewee.' preamble? -> only if you do a * import
class = table
model = file where you are saving the classes/tables -> like a db essentially
'''
# C:\Users\v-ollock\AppData\Local\Programs\Python\Python37-32\Lib\sqlite3
# http://zetcode.com/python/peewee/

from peewee import SqliteDatabase, Model, CharField, DecimalField


db = SqliteDatabase('Gibbs.db')
# db.connect()
# db.execute_sql("PRAGMA foreign_keys = ON;")


class BaseModel(Model):
    """Peewee meta class.  Assign db and table"""
    class Meta:
        database = db  # database is a keyword


class Customer(BaseModel):
    """ class = model = table"""
    # customer_id = IdentityField() or AutoField()
    # the videos said use your 'business sense' for primary key
    name = CharField(primary_key=True, max_length=50)
    last_name = CharField(max_length=50)
    home_address = CharField(max_length=50)
    phone_number = CharField(max_length=20)
    email_address = CharField(max_length=50)
    status = CharField(max_length=50)
    poverty_score = DecimalField(max_digits=3, decimal_places=0)
