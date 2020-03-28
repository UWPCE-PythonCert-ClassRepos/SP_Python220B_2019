#!/usr/bin/env python
"""
Customized fields for use in customer_model module.
"""

from peewee import CharField


class ActiveField(CharField):
    """
    Custom class for the customer's entry as 'active' or 'inactive'.
    """

    def db_value(self, value):
        if value in ['active', 'inactive']:
            return value
        else:
            raise ValueError("Entry must be 'active' or 'inactive'.")


class CustIDField(CharField):
    """
    Custom class for the format of the customer's ID.
    """

    def db_value(self, value):
        if value[0:2].isupper() and value[2:6].isdigit() and len(value) == 6:
            return value
        else:
            raise ValueError("Entry format is 'xxyyyy' where 'x' is an uppercase letter, and 'y' "
                             "is a digit.")


class PhoneField(CharField):
    """
    Custom class for the format of the customer's phone number.
    """

    def db_value(self, value):
        if len(value) == 10 and value[:].isdigit():
            return value
        else:
            raise ValueError("Phone number must be 10 digits, with no other characters.")


class CreditField(CharField):
    """
    Custom class for the format of the customer's credit limit.
    """

    def db_value(self, value):
        if value[:].isdigit():
            return value
        else:
            raise ValueError("Credit characters must be digits only.")
