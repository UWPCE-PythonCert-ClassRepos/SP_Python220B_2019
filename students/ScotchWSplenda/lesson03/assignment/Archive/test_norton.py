from peewee import *
from basic_ops import *
from customer_model import Customer, db
import sqlite3



# https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm
# conn = sqlite3.connect('customer.db')
# cursor = conn.cursor()
# cursor.execute("DROP TABLE Customer")
# print("Table dropped... ")
# conn.commit()
# conn.close()


# DB = SqliteDatabase('customer.db')
# DB.connect()
# DB.execute_sql('PRAGMA foreign_keys = ON;')  # needed for sqlite only
#
# Customer.drop_table()
# DB.drop_tables([Customer])
# DB.create_tables([Customer])

customer1 = {
    'name': 'Freddie',
    'lastname': 'Gibbs',
    'home_address': '123 Fake St',
    'phone_number': '206-360-4200',
    'email_address': 'fgibbs@washington.edu',
    'status': True,
    'poverty_score': 420}

# customer2 = {
#     'name': 'Gangsta',
#     'lastname': 'Gibbs',
#     'home_address': '420 Fake Blvd',
#     'phone_number': '206-699-4200',
#     'email_address': 'ggibbs@washington.edu',
#     'status': True,
#     'poverty_score': 900}
#
# customer3 = {
#     'name': 'Skinny',
#     'lastname': 'Suge',
#     'home_address': '69 Fake Ave',
#     'phone_number': '206-690-4000',
#     'email_address': 'ssuge@washington.edu',
#     'status': True,
#     'poverty_score': 690}
#
# x = search_customer('Freddie')
# print(x)

# add_customer(**customer1)
# add_customer(**customer2)
# add_customer(**customer3)


x = Customer.select()

for i in x:
    print(i.name)
