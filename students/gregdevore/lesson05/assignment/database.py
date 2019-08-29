'''
This file contains functions for converting CSV data to a MongoDB database
'''

def import_data(directory_name, product_file, customer_file, rentals_file):
    '''
    This function takes a directory name three csv files as input, one with
    product data, one with customer data and the third one with rentals data
    and creates and populates a new MongoDB database with these data. It
    returns 2 tuples: the first with a record count of the number of
    products, customers and rentals added (in that order), the second with a
    count of any errors that occurred, in the same order.
    '''
    pass

def show_available_products():
    '''
    Returns a Python dictionary of products listed as available with the following fields:
        product_id.
        description.
        product_type.
        quantity_available.

        {
        ‘prd001’:
            {‘description’:‘60-inch TV stand’,
            ’product_type’:’livingroom’,
            ’quantity_available’:‘3’},
        ’prd002’:
            {‘description’:’L-shaped sofa’,
            ’product_type’:’livingroom’,
            ’quantity_available’:‘1’}
        }
    '''
    pass

def show_rentals(product_id):
    '''
    Returns a Python dictionary with the following user information from users that have rented products matching product_id:
        user_id.
        name.
        address.
        phone_number.
        email.

        {
        ‘user001’:
            {‘name’:’Elisa Miles’,
            ’address’:‘4490 Union Street’,
            ’phone_number’:‘206-922-0882’,
            ’email’:’elisa.miles@yahoo.com’},
        ’user002’:
            {‘name’:’Maya Data’,
            ’address’:‘4936 Elliot Avenue’,
            ’phone_number’:‘206-777-1927’,
            ’email’:’mdata@uw.edu’}}
    '''
    pass
