"""File for running the commands and timeing then for comparison"""



from .linear import *

insert_into_table(os.getcwd() + '\\', 'HP_Norton_products.csv', 'HP_Norton_customers.csv', 'HP_Norton_rentals.csv')
