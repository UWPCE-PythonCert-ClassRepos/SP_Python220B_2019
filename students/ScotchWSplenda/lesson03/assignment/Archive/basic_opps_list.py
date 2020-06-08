"""

how can I print it nicely instead of these ugly tuples?
who don't i have to 'connect' or 'close'?
"""

from customer_model import db, Customer
import peewee
#
#
Customer.create_table()
# Customer.drop_table()

# # creating definitions for tuple index
# NAME = 0
# LASTNAME = 1
# ADDRESS = 2
# PHONE = 3
# EMAIL = 4
# STATUS = 5
# LIMIT = 6
#

def add_customer(customer_data):
    for guy in customer_data:
        try:
            with db.transaction():
                new_customer = Customer.create(
                    name=guy[0],
                    last_name=guy[1],
                    home_address=guy[2],
                    phone_number=guy[3],
                    email_address=guy[4],
                    status=guy[5],
                    poverty_score=guy[6]
                    )
                new_customer.save()
        except peewee.IntegrityError:
            print('IntegrityError, Error adding customer %s', guy)

# has to be in brackets if its a list
stank = [('sdfsdfsdf', 'butt', '123 spring ave', 2223334456,
         'fart@gmail.com', True, 220)]


add_customer(stank)


x = Customer.select()
# have to make it a list
# x = [i for i in x.tuples()]
for y in x:
    print(y.name)
