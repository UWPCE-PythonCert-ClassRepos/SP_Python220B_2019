'''
    create 3 csv files
    pylint disable=unused-variable
'''
import csv
import random

def customer_file():
    '''create expanded rentals file'''
    with open('csv_files/customer_file.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        customer_num = 9
        for i in range(900):
            customer_num += 1
            spamwriter.writerow(['cid' + f'{customer_num}']+
                                ['JohnSmith '+f'{customer_num}']+
                                [str(random.randrange(10000, 99999)) + ' SomeStreet Ave']+
                                [random.randrange(1000000000, 9999999999)]+
                                ['JohnSmith'+f'{customer_num}'+'@gmail.com'])

def product_file():
    '''create expanded rentals file'''
    with open('csv_files/product_file.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        product_num = 9
        for i in range(900):
            product_num += 1
            spamwriter.writerow(['pid' + str(product_num)]+
                                ['Appliance ' + str(product_num)]+
                                ['Kitchen']+
                                [random.randrange(30, 60)])

def rentals_file():
    '''create expanded rentals file'''
    with open('csv_files/rentals_file.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        customer_num = 99
        for i in range(900):
            customer_num += 1
            spamwriter.writerow(['rid' + str(customer_num)]+
                                ['pid' + str(customer_num)]+
                                ['cid'+ str(customer_num)])


if __name__ == '__main__':
    customer_file()
    product_file()
    rentals_file()
