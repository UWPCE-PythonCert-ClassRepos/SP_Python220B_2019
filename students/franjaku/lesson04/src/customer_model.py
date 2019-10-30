"""
    Definition of the customer model that is needed for the HP Norton database.
    As the project grows in scope we can expand the models (tables) needed for the database.
"""

import peewee as pw

database = pw.SqliteDatabase('customer_database.db')


class BaseModel(pw.Model):
    """Base clase...."""
    class Meta:
        """Connects all the models to one database."""
        database = database


class Customer(BaseModel):
    """
        Defines the customer table for the database.
        Customer ID will be used as the primary key.

        Fields
            -Customer ID (primary key)
            -Name
            -Last name
            -Home address
            -Phone number
            -Email address
            -Status (active or inactive)
            -Credit limit
    """
    customer_id = pw.IntegerField(primary_key=True)
    name = pw.CharField(max_length=30)
    last_name = pw.CharField(max_length=30)
    home_address = pw.CharField()
    phone_number = pw.CharField(max_length=10)
    email_address = pw.CharField()
    status = pw.CharField(null=False)
    credit_limit = pw.IntegerField(null=False)


database.create_tables([Customer])
