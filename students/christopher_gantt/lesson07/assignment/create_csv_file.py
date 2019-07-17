'''
    create 3 csv files
    pylint disable=unused-variable
'''
import csv
import random

def customer_file():
    '''creates a customer file with 900 entries'''
    with open('csv_files/customer_file.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        customer_num = 99
        for i in range(900):
            customer_num += 1
            spamwriter.writerow(['c' + f'{customer_num}']+
                                ['John '+f'{customer_num}']+
                                [str(random.randrange(10000, 99999)) + ' Imaginary St. W']+
                                [random.randrange(1000000000, 9999999999)]+
                                ['John'+f'{customer_num}'+'@gmail.com'])

def product_file():
    '''creates a product file with 900 entries'''
    with open('csv_files/product_file.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        product_num = 99
        for i in range(900):
            product_num += 1
            spamwriter.writerow(['p' + str(product_num)]+
                                ['Product ' + str(product_num)]+
                                ['Kitchen']+
                                [random.randrange(0, 30)])

def rentals_file():
    '''creates a rentals file with 900 entries'''
    with open('csv_files/rentals_file.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        customer_num = 99
        for i in range(900):
            customer_num += 1
            spamwriter.writerow(['c' + str(customer_num)]+
                                ['John ' + str(customer_num)]+
                                ['p'+str(random.randrange(100, 999))])


if __name__ == '__main__':
    customer_file()
    product_file()
    rentals_file()
