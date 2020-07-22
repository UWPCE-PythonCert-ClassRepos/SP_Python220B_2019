'''test inventory'''

from inventory import add_furniture, single_customer

add_furniture("rented_items.csv", "Elisa Miles", "LR04", "Leather Sofa", 25)
add_furniture("rented_items.csv", "Edward Data", "KT78", "Kitchen Table", 10)
add_furniture("rented_items.csv", "Alex Gonzales", 'BR02', "Queen Mattress", 17)
CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
CREATE_INVOICE("test_items.csv")
