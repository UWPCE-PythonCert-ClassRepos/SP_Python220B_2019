import csv
from random import randint
import random
from faker import Faker

faker = Faker()
profile = faker.profile()

brand_name = ['Dania ', 'La-Z-Boy ', 'Ashley ', 'Bernhardt ', 'Crate&Barrel ']
product_desc = ['Lift chair', 'Bean bag', 'Chaise longue', 'Fauteuil', 'Ottoman',
                'Recliner', 'Stool', 'Bar Stool', 'Footstool', 'Tuffet', 'Fainting couch',
                'Rocking chair', 'Bar chair', 'Bench', 'Accubita', 'CanapŽ', 'Davenport',
                'Klinai', 'Divan', 'Love seat', 'Chesterfield', 'Bed', 'Bunk bed',
                'Canopy bed', 'Four-poster bed', 'Murphy bed', 'Platform bed', 'Sleigh bed',
                'Waterbed', 'Daybed', 'Futon', 'Hammock', 'Headboard',
                'crib', 'cradle', 'Sofa bed', 'Toddler bed', 'Entertainment', 'A coat rack',
                'Drawer', 'Hall tree', 'Hatstand', 'Bar cabinet', 'Filing cabinet',
                'Floating shelf', 'Nightstand', 'Ottoman', 'Plan chest', 'Shelving',
                'Sideboard', 'Safe', 'Umbrella stand', 'An umbrella', 'Wardrobe',
                'Wine rack', 'bedroom set', 'Dinette (group)','Dining set', 'Vanity set',
                'Lamp']

product_type = ['livingroom', 'kitchen', 'bedroom']


def expand_data(customer_file, product_file, rental_file):
	"""expand data to 1000 records"""
	with open(customer_file, 'w', newline='') as customer_file:
		fieldnames = ['user_id', 'name', 'address', 'phone_number', 'email']
		writer = csv.DictWriter(customer_file, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(1, 1001):
			user_id = "User{0:03}".format(i)
			writer.writerow({'user_id': user_id,
			                 'name': faker.name(),
			                 'address': faker.address(),
			                 'phone_number': faker.phone_number(),
			                 'email': faker.email()})

	with open(product_file, 'w', newline='') as product_file:
		fieldnames = ['product_id', 'description', 'product_type', 'quantity_available']
		writer = csv.DictWriter(product_file, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(1, 1001):
			product_id = "prd{0:03}".format(i)
			writer.writerow({'product_id': product_id,
			                 'description': random.choice(brand_name) + random.choice(
				                 product_desc),
			                 'product_type': random.choice(product_type),
			                 'quantity_available': randint(0, 10)})

	with open(rental_file, 'w', newline='') as rental_file:
		fieldnames = ['product_id', 'user_id']
		writer = csv.DictWriter(rental_file, fieldnames=fieldnames)
		writer.writeheader()
		for i in range(1, 1001):
			product_id = "prd{0:03}".format(randint(0, 1001))
			user_id = "User{0:03}".format(randint(0, 1001))
			writer.writerow({'product_id': product_id,
			                 'user_id': user_id})


if __name__ == "__main__":
	expand_data('customers.csv', 'product.csv', 'rental.csv')
