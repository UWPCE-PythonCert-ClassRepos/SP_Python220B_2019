import csv
import random


first_names = ['Aaron', 'Bill', 'Charley', 'Dave',
               'Elijah', 'Frank', 'George', 'Harry',
               'Idris', 'Jerry', 'Karl', 'Lenny',
               'Mike', 'Nate', 'Oscar', 'Pete',
               'Q', 'Red', 'Steve', 'Terry', 'Ulysses',
               'Victor', 'Warren', 'Xander', 'Yuri', 'Zed']

last_names = ['Carlson', 'Mcmillan', 'Pope', 'Reese',
              'Hoover', 'Cervantes', 'Santiago', 'Houston',
              'Andrade', 'Gibson', 'Cole', 'Frost', 'Moore',
              'Compton', 'Blake', 'Pena', 'Pace', 'Kirby',
              'Hudson', 'Phelps', 'Pitts', 'Mays', 'Casey',
              'Hernandez', 'Mullins', 'Todd']

addresses = ['8949 West Delaware Ave.', '7685 Piper St.',
             '846 James Ave.', '274 George St.', '11 Wayne Rd.',
             '54 Bay Street', '556 Franklin Dr.', '144 Fawn Dr.',
             '5 Smoky Hollow Ave.', '930 Peninsula Street',
             '58 Brewery Street', '3 Bank Dr.', '879 Woodsman Lane',
             '87 East Acacia St.', '32 Rocky River Dr.',
             '802 Wayne Street', '8907 Hartford St.',
             '8761 North Dr.', '7262 Marlborough St.',
             '384 Carriage Street', '9865 Canal Street',
             '7798 West Bay Meadows Street',
             '699 Arch St.', '40 Ramblewood St.', '166 Lookout St.',
             '106 Sage Street']

phones = ['(291) 991-3613', '(484) 611-7271', '(535) 219-8331',
          '(680) 889-4277', '(213) 759-0227', '(776) 306-1111',
          '(736) 777-4851', '(513) 465-2638', '(878) 371-3922',
          '(662) 255-5500', '(694) 547-4859', '(358) 865-0197',
          '(684) 837-4209', '(872) 208-7807', '(259) 918-3153',
          '(461) 973-0480', '(685) 645-7985', '(988) 479-5775',
          '(269) 776-8706', '(699) 943-1537', '(699) 521-0897',
          '(610) 842-4284', '(470) 594-8260', '(534) 985-2899',
          '(648) 252-6439', '(510) 398-8826']

emails = ['gmail.com', 'outlook.com', 'mac.com', 'yahoo.com', 'aol.com']

products = ['bananas', 'thread', 'nail clippers', 'CD', 'drawer',
            'cookie jar', 'drill press', 'soap', 'spring', 'speakers',
            'lamp', 'brocolli', 'sticky note', 'bottle cap', 'deodorant',
            'car', 'ipod', 'pen', 'sandal', 'sofa', 'key chain', 'rug',
            'sketch pad', 'toothpaste', 'sidewalk', 'towel', 'checkbook',
            'USB drive', 'bowl', 'mouse pad']

product_cats = ['TV', 'Furniture', 'Kitchen', 'Bedroom', 'Accessories']

with open('customers.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',')

    for i in range(1000):

        cust_id = 'cust' + '{:04d}'.format(i)
        first_name = first_names[random.randint(0, 25)]
        last_name = last_names[random.randint(0, 25)]
        address = addresses[random.randint(0, 25)]
        phone = phones[random.randint(0, 25)]
        email = first_name[0] + last_name + '@' + emails[random.randint(0, 4)]

        data_writer.writerow([cust_id, first_name + ' ' + last_name,
                              address, phone, email])

with open('products.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',')

    for i in range(1000):

        prd_id = 'prd' + '{:04d}'.format(i)
        product = products[random.randint(0, 29)]
        cat = product_cats[random.randint(0, 4)]
        inv_ct = random.randint(0, 5)

        data_writer.writerow([prd_id, product, cat, inv_ct])

with open('rentals.csv', mode='w') as data_file:
    data_writer = csv.writer(data_file, delimiter=',')

    for i in range(1000):

        rnt_id = 'rnt' + '{:04d}'.format(i)
        prd_id = 'prd' + '{:04d}'.format(random.randint(0, 999))
        cust_id = 'cust' + '{:04d}'.format(random.randint(0, 999))

        data_writer.writerow([rnt_id, prd_id, cust_id])

