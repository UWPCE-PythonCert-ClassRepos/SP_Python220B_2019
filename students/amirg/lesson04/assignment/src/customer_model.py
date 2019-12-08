'''
This module contains the customer model'''
import peewee as p

DB = p.SqliteDatabase('customers.db')

class BaseModel(p.Model):
    '''
    This class sets up the base model
    '''
    class Meta: #pylint: disable=too-few-public-methods
        '''
        This class is meta of the basemodel
        '''
        database = DB

class Customer(BaseModel):
    '''
    This class sets up the customer model
    '''
    customer_id = p.IntegerField(primary_key=True)
    name = p.CharField(max_length=20)
    lastname = p.CharField(max_length=20)
    home_address = p.CharField(max_length=100)
    phone_number = p.CharField(max_length=10)
    email_address = p.CharField(max_length=50)
    status = p.CharField(max_length=8)
    credit_limit = p.IntegerField()

#instantiates customer database
DB.create_tables([Customer])
