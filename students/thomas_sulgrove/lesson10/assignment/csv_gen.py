'''A script to build a butt load of csv values to test the parallization on'''

from random import randint
import csv
import os
import os.path
from faker import Faker


# pylint: disable=too-many-locals

def csv_gen(desired_row_count, product_file_name, cust_file_name, rental_file_name):
    """quickly making this a function so can be called elsewhere"""
    desired_row_count = desired_row_count - 1  # b/c python

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
    if os.path.isfile(cust_file_name):
        os.remove(cust_file_name)
    with open(cust_file_name, 'w+') as file:
        row_num = sum(1 for line in csv.reader(file))
        while row_num <= desired_row_count:

            if row_num == 0:
                file.write('user_id,name,address,phone,email')
            new_row = (
                '\nuser{},{},{},{},{}'.format(str(row_num).zfill(len(str(desired_row_count))),
                                              fake.name(), fake.address().replace("\n", " "),
                                              fake.phone_number(), fake.email()))

            file.write(new_row)
            row_num += 1

    if os.path.isfile(product_file_name):
        os.remove(product_file_name)
    with open(product_file_name, 'w+') as file:
        row_num = sum(1 for line in csv.reader(file))

        while row_num <= desired_row_count:
            if row_num == 0:
                file.write('product_id,description,product_type,quantity_available')
            furniture_name = descriptions[randint(0, len(descriptions) - 1)] + ' ' + \
                             material[randint(0, len(material) - 1)] + ' ' + \
                             furniture[randint(0, len(furniture) - 1)]
            furniture_room = room[randint(0, len(room) - 1)]
            new_row = ('\nprod{},{},{},{}'.format(str(row_num).zfill(len(str(desired_row_count))),
                                                  furniture_name, furniture_room, randint(0, 100)))
            file.write(new_row)
            row_num += 1

    if os.path.isfile(rental_file_name):
        os.remove(rental_file_name)
    with open(rental_file_name, 'w+') as file:
        row_num = sum(1 for line in csv.reader(file))
        while row_num <= desired_row_count:
            if row_num == 0:
                file.write('rental_id,product_id,customer_id,amount,time,price,total')
            amount = randint(0, 100)
            time = randint(0, 365)
            price = randint(0, 500)
            total = amount * time * price

            new_row = ('\nrnt{},prd{},user{},{},{},{},{}'.format(
                str(row_num).zfill(len(str(desired_row_count))),
                randint(0, desired_row_count),
                str(row_num).zfill(len(str(desired_row_count))),
                amount, time, price, total))

            file.write(new_row)
            row_num += 1
