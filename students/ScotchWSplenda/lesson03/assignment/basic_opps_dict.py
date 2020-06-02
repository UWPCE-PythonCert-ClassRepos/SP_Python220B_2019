"""


who don't i have to 'connect' or 'close'?
"""

from customer_model import db, Customer
import peewee
#
#
Customer.create_table()
# Customer.drop_table()


def add_customer(_name, _lastname, _home_address, _phone_number,
                 _email_address, _status, _poverty_score):
    '''add new customer function.'''
    with db.transaction():
        new_customer = Customer.create(
                    name=_name,
                    last_name=_lastname,
                    home_address=_home_address,
                    phone_number=_phone_number,
                    email_address=_email_address,
                    status=_status,
                    poverty_score=_poverty_score
                    )
        new_customer.save()


customer1 = {
    '_name': 'Freddie',
    '_lastname': 'Gibbs',
    '_home_address': '123 Fake St',
    '_phone_number': '206-360-4200',
    '_email_address': 'fgibbs@washington.edu',
    '_status': True,
    '_poverty_score': 420}

# add_customer(**customer1)


x = Customer.select()
# have to make it a list
x = [i for i in x.tuples()]
print(x)
