'''
Peewee ORM, sqlite and Python
'''
# C:\Users\v-ollock\AppData\Local\Programs\Python\Python37-32\Lib\sqlite3
# http://zetcode.com/python/peewee/

import peewee

db = peewee.SqliteDatabase('Norton.db')


class Customer(peewee.Model):
    """ class = model = table"""
    # customer_id = IdentityField() or AutoField()
    # the videos said use your 'business sense' for primary key
    name = peewee.CharField(primary_key=True, max_length=50)
    last_name = peewee.CharField(max_length=50)
    home_address = peewee.CharField(max_length=50)
    phone_number = peewee.CharField(max_length=20)
    email_address = peewee.CharField(max_length=50)
    status = peewee.BooleanField()
    poverty_score = peewee.DecimalField(max_digits=3, decimal_places=0)

    class Meta:
        """Peewee meta class.  Assign db and table"""
        database = db
        db_table = 'customer'


Customer.create_table()
