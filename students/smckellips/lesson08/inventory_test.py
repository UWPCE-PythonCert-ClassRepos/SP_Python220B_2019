# pylint: disable=C0103
'''
Test utility for HP Norton Inventory System Version 8.
'''
from inventory import add_furniture, single_customer

add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
#Sample data was missing item_code
add_furniture("rented_items.csv", "Alex Gonzales", "BR01", "Queen Mattress", 17)
create_invoice = single_customer("Susan Wong", "rented_items.csv")
create_invoice("test_items.csv")
