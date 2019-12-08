'''A script to build a butt load of csv values to test the parallization on'''
'''customers.csv example
user_id,name,address,phone,email
user001,Guy Dudeman,1139 Bro Street,800-123-4567,Guy_Dudeman01@gmail.com
user002,Man Dudeguy,3729 High Five Ave,800-234-5678,Man_Guydude31@gmail.com
user003,Jenny Anylady,1000 Baltimore Blvd,800-123-4567,Dontchangeyournumber@gmail.com
user004,Felice Gertrude,1000 1st Street,800-000-0000,Knits4kicks@gmail.com.com
user005,Walt Kowalski,238 Rhode Island Street,800-000-0001,getoffmylawn@gmail.com
'''

'''products.csv
product_id,description,product_type,quantity_available
prd001,60-inch TV stand,livingroom,3
prd002,couch,livingroom,5
prd003,microwave,kitchen,2
prd004,nightstand,bedroom,17
prd005,bed frame,bedroom,1
'''

'''rentals.csv
rental_id,product_id,customer_id,amount,time,price,total
rnt001,prd001,user001,1,7,10,70
rnt002,prd005,user002,1,14,20,280
rnt003,prd002,user003,'5,3,20,60
rnt004,prd003,user004,2,2,10,20
rnt005,prd001,user005,1,7,70,490
'''

from random import randrange, randint
from datetime import datetime, timedelta
import csv
import os
from faker import Faker

fake = Faker()

descriptions = ('Big', 'Colossal', 'Fat', 'Gigantic', 'Great',
                'Huge', 'Immense', 'Large', 'Little', 'Mammoth', 'Massive',
                'Microscopic', 'Miniature', 'Petite', 'Puny', 'Scrawny', 'Short',
                'Small', 'Tall', 'Tiny')

material = ('Steel', 'Iron', 'Aluminum', 'Magnesium', 'Copper',
            'Brass', 'Bronze', 'Zinc', 'Magnesium', 'Titanium',
            'Tungsten', 'Adamantium', 'Nickel', 'Cobalt', 'Tin',
            'Lead', 'Pine', 'Cedar', 'Oak', 'Ash',
            'Beech', 'Elm', 'Mahogany', 'Teak', 'Walnut',
            'Granite', 'Limestone', 'Slate', 'Marble', 'Quartzite',
            'Sandstone', 'Travertine', 'Basalt')

furniture = ('Chair', 'Lift chair', 'Bean bag', 'Chaise longue', 'Fauteuil',
             'Ottoman', 'Recliner', 'Stool', 'Bar Stool', 'Footstool',
             'Tuffet', 'Fainting couch', 'Rocking chair', 'Bar chair', 'Bench',
             'Couch', 'Accubita', 'Canapé', 'Davenport', 'Klinai',
             'Divan', 'Love seat', 'Chesterfield', 'Bed', 'Bunk bed',
             'Canopy bed', 'Four-poster bed', 'Murphy bed', 'Platform bed', 'Sleigh bed',
             'Waterbed', 'Daybed', 'Futon', 'Hammock', 'Headboard',
             'Infant bed', 'Mattress', 'Sofa')

room = ('kitchen', 'living room', 'bathroom', 'closet', 'den', 'attic', 'dining room')

file_name = 'HP_Norton_customers.csv'
desired_row_count = 1000000
desired_row_count -= 1 # b/c python

with open(file_name, 'w+') as file:
    row_num = sum(1 for line in csv.reader(file))
    print(row_num)
    while row_num <= desired_row_count:
        if row_num == 0:
            file.write('user_id,name,address,phone,email')
            next
        new_row = (
            '\nuser{},{},{},{},{}'.format(str(row_num).zfill(len(str(desired_row_count))), fake.name(),
                                          fake.address().replace("\n", " "), fake.phone_number(),
                                          fake.email()))
        file.write(new_row)
        row_num += 1
        print(row_num / desired_row_count)

file_name = 'HP_Norton_products.csv'
with open(file_name, 'w+') as file:
    row_num = sum(1 for line in csv.reader(file))

    while row_num <= desired_row_count:
        if row_num == 0:
            file.write('product_id,description,product_type,quantity_available')
            next
        furniture_name = descriptions[randint(0, len(descriptions) - 1)] + ' ' + \
                         material[randint(0, len(material) - 1)] + ' ' + \
                         furniture[randint(0, len(furniture) - 1)]
        furniture_room = room[randint(0, len(room) - 1)]
        new_row = ('\nprod{},{},{},{}'.format(str(row_num).zfill(len(str(desired_row_count))), furniture_name,
                                            furniture_room, randint(0, 100)))
        file.write(new_row)
        row_num += 1

file_name = 'HP_Norton_rentals.csv'
with open(file_name, 'w+') as file:
    row_num = sum(1 for line in csv.reader(file))
    while row_num <= desired_row_count:
        if row_num == 0:
            file.write('rental_id,product_id,customer_id,amount,time,price,total')
            next
        amount = randint(0, 100)
        time = randint(0, 365)
        price = randint(0, 500)
        total = amount * time * price

        new_row = ('\nrnt{},prd{},user{},{},{},{},{}'.format(str(row_num).zfill(len(str(desired_row_count))),
                                                           randint(0, desired_row_count),
                                                           str(row_num).zfill(len(str(desired_row_count))),
                                                           amount, time, price, total))

        file.write(new_row)
        row_num += 1
