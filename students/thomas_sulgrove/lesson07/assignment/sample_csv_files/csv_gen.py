"""A script to build a butt load of csv values to test the parallization on"""

from random import randint
import csv
from faker import Faker

FAKE = Faker()

DESCRIPTIONS = ('Big', 'Colossal', 'Fat', 'Gigantic', 'Great',
                'Huge', 'Immense', 'Large', 'Little', 'Mammoth', 'Massive',
                'Microscopic', 'Miniature', 'Petite', 'Puny', 'Scrawny', 'Short',
                'Small', 'Tall', 'Tiny')

MATERIAL = ('Steel', 'Iron', 'Aluminum', 'Magnesium', 'Copper',
            'Brass', 'Bronze', 'Zinc', 'Magnesium', 'Titanium',
            'Tungsten', 'Adamantium', 'Nickel', 'Cobalt', 'Tin',
            'Lead', 'Pine', 'Cedar', 'Oak', 'Ash',
            'Beech', 'Elm', 'Mahogany', 'Teak', 'Walnut',
            'Granite', 'Limestone', 'Slate', 'Marble', 'Quartzite',
            'Sandstone', 'Travertine', 'Basalt')

FURNITURE = ('Chair', 'Lift chair', 'Bean bag', 'Chaise longue', 'Fauteuil',
             'Ottoman', 'Recliner', 'Stool', 'Bar Stool', 'Footstool',
             'Tuffet', 'Fainting couch', 'Rocking chair', 'Bar chair', 'Bench',
             'Couch', 'Accubita', 'Canapé', 'Davenport', 'Klinai',
             'Divan', 'Love seat', 'Chesterfield', 'Bed', 'Bunk bed',
             'Canopy bed', 'Four-poster bed', 'Murphy bed', 'Platform bed', 'Sleigh bed',
             'Waterbed', 'Daybed', 'Futon', 'Hammock', 'Headboard',
             'Infant bed', 'Mattress', 'Sofa')

ROOM = ('kitchen', 'living room', 'bathroom', 'closet', 'den', 'attic', 'dining room')

FILE_NAME = 'HP_Norton_customers.csv'
DESIRED_ROW_COUNT = 1000000
DESIRED_ROW_COUNT -= 1 # b/c python

with open(FILE_NAME, 'w+') as file:
    ROW_NUM = sum(1 for line in csv.reader(file))
    while ROW_NUM <= DESIRED_ROW_COUNT:
        if ROW_NUM == 0:
            file.write('user_id,name,address,phone,email')
        NEW_ROW = (
            '\nuser{},{},{},{},{}'.format(str(ROW_NUM).zfill(len(str(
                DESIRED_ROW_COUNT))), FAKE.name(),
                                          FAKE.address().replace("\n", " "), FAKE.phone_number(),
                                          FAKE.email()))

        file.write(NEW_ROW)
        ROW_NUM += 1
        print(ROW_NUM / DESIRED_ROW_COUNT)

FILE_NAME = 'HP_Norton_products.csv'
with open(FILE_NAME, 'w+') as file:
    ROW_NUM = sum(1 for line in csv.reader(file))

    while ROW_NUM <= DESIRED_ROW_COUNT:
        if ROW_NUM == 0:
            file.write('product_id,description,product_type,quantity_available')
        FURNITURE_NAME = DESCRIPTIONS[randint(0, len(DESCRIPTIONS) - 1)] + ' ' + \
                         MATERIAL[randint(0, len(MATERIAL) - 1)] + ' ' + \
                         FURNITURE[randint(0, len(FURNITURE) - 1)]
        FURNITURE_ROOM = ROOM[randint(0, len(ROOM) - 1)]
        NEW_ROW = ('\nprod{},{},{},{}'.format(str(ROW_NUM).zfill(len(str(
            DESIRED_ROW_COUNT))), FURNITURE_NAME,
                                              FURNITURE_ROOM, randint(0, 100)))
        file.write(NEW_ROW)
        ROW_NUM += 1

FILE_NAME = 'HP_Norton_rentals.csv'
with open(FILE_NAME, 'w+') as file:
    ROW_NUM = sum(1 for line in csv.reader(file))
    while ROW_NUM <= DESIRED_ROW_COUNT:
        if ROW_NUM == 0:
            file.write('rental_id,product_id,customer_id,amount,time,price,total')
        AMOUNT = randint(0, 100)
        TIME = randint(0, 365)
        PRICE = randint(0, 500)
        TOTAL = AMOUNT * TIME * PRICE

        NEW_ROW = ('\nrnt{},prd{},user{},{},{},{},{}'.format(str(ROW_NUM).zfill(len(str(
            DESIRED_ROW_COUNT))), randint(0, DESIRED_ROW_COUNT), str(ROW_NUM).zfill(len(str(
                DESIRED_ROW_COUNT))), AMOUNT, TIME, PRICE, TOTAL))

        file.write(NEW_ROW)
        ROW_NUM += 1
