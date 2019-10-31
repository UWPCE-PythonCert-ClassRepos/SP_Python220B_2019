from random import randint
import csv

first_name=['Lisa', 'Pooria', 'John', 'Ella', 'meysam']
last_name=['Miles', 'boston', 'wing', 'Bella', 'tahami']
street_name = ['dexter Ave', '7th Ave', 'Elliot bay', 'pike palce']

def create_customer(id):
    customer_id = 'user' + str(id).zfill(3)
    name = '{} {}'.format(first_name[randint(0, len(first_name)-1)], last_name[randint(0, len(last_name)-1)])
    email = name.replace(" ", "_") + '@gmail.com'
    customer_address = '{} {}'.format(randint(100,450),street_name[randint(0,len(street_name)-1)])
    customer_phone = '{}-{}-{}'.format(randint(200,700),randint(200,700),randint(200,700))
    customer_info = customer_id + ','+ name +',' + email + ',' + customer_address +','+ customer_phone
    return customer_info


def create_rental(id):
    rental_info = "prd" + str(randint(1,2)).zfill(3) + ',' + 'user' + str(randint(1,20)).zfill(3) + ',' + str(randint(1,5))
    return rental_info


def write_to_csv(file_name, a_string):
    with open (file_name, 'a') as csv_file:
        csv_file.write(a_string)
        csv_file.write('\n')
        csv_file.close()


for x in range(1,21):
    new_customer = create_customer(x)
    new_rental = create_rental(x)
    write_to_csv('customer_csv',new_customer)
    write_to_csv('rental_csv', new_rental)
    print (create_customer(x))
    print (create_rental(x))


