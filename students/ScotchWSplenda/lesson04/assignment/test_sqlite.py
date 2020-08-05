'''
doesnt work when i put it in the subfolder 'tests''

if i indent the 'customers' dicts under def setup they dont get recognized
in the lower down methods, something to do with 'self'

the db gets created without being explicitly told to do so
'''
from basic_opps_dict2 import (delete_customer, add_customer, search_customer,
                              update_customer_credit, list_active_customers)

from customer_model import db, Customer


def setup(self):
    '''sdfdsf'''
    db.drop_tables([Customer])
    db.create_tables([Customer])
    # self.database.close()
    # Customer.drop_table()
    # Customer.create_table()


customer2 = {
    '_name': 'Gangsta',
    '_last_name': 'Gibbs',
    '_home_address': '420 Fake Blvd',
    '_phone_number': '206-699-4200',
    '_email_address': 'ggibbs@washington.edu',
    '_status': True,
    '_poverty_score': 900}
customer3 = {
    '_name': 'Skinny',
    '_last_name': 'Suge',
    '_home_address': '69 Fake Ave',
    '_phone_number': '206-690-4000',
    '_email_address': 'ssuge@washington.edu',
    '_status': True,
    '_poverty_score': 690}
customer1 = {
    '_name': 'Freddie',
    '_last_name': 'Gibbs',
    '_home_address': '123 Fake St',
    '_phone_number': '206-360-4200',
    '_email_address': 'fgibbs@washington.edu',
    '_status': True,
    '_poverty_score': 420
    }


add_customer(**customer1)
delete_customer('Freddie')
add_customer(**customer2)
search_customer('Gangsta')
add_customer(**customer3)
update_customer_credit('Skinny', 100)
add_customer(**customer1)
add_customer(**customer2)
print(list_active_customers())
