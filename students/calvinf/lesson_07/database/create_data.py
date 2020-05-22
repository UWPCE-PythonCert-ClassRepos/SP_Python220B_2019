from random import randint, choice
import csv


def random_one_product(num_of_rows):
    for row in range(num_of_rows):
        row += 1
        desccolumn = choice(['60 - inch TV stand', 'Black 240 watt Oven ', 'Brown faux fur love seat', 'U - shaped Love seat'])
        prdcolumn = choice(['livingroom', 'Outdoor', 'Bathroom', 'Kitchen'])
        quantcolumn = randint(0, 25)
        yield ["prd" + str(row), desccolumn, prdcolumn, quantcolumn]


def random_one_customer(num_of_rows):
    for row in range(num_of_rows):
        row += 1
        first_names = choice(['John', 'Andy', 'Joe', 'Calvin', 'Stephen', 'Elisa'])
        last_names = choice(['Johnson', 'Smith', 'Williams', 'King', 'Hunt', 'Miles'])
        address = choice(['3145 Woodlane', '7853 Elliot Ave', '4566 Cherry Street', '498789 Moolokiaiin'])
        areacode = choice(['206','425', '253'])
        phone1 = randint(200, 899)
        phone2 = randint(200, 899)
        phonenumber = str(areacode) + "-" + str(phone1) + "-" + str(phone2)
        endemail = choice(['@uw.edu', '@gmail.com', '@hotmail.com'])
        email = first_names + "." + last_names + endemail
        yield ["user" + str(row), first_names, last_names, address, phonenumber, email]


def random_one_rental(num_of_rows):
    for row in range(num_of_rows):
        row += 1
        customer = randint(1, 10000)
        prdcolumn = randint(1, 10000)
        yield ["rnt" + str(row), "user" + str(customer), "prd" + str(prdcolumn)]


def create_csv():
    rownum = 10000
    with open('products.csv', "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['product_id', 'description', 'product_type', 'quantity'])
        for line in random_one_product(rownum):
            writer.writerow(line)
            # print(line)
    with open('customer.csv', "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['user_id', 'first_name', 'last_name', 'address', 'phone_number', 'email'])
        for line in random_one_customer(rownum):
            writer.writerow(line)

    with open('rental.csv', "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['rental_id', 'user_id', 'product_id'])
        for line in random_one_rental(10000):
            writer.writerow(line)


if __name__ == '__main__':
    create_csv()
