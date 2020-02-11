import csv
import random
import string

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def random_products(directory_name, product_file):
    file_name = directory_name + product_file
    count = 3
    with open(file_name, 'a', newline='') as csvfile:
        for i in range(0, 1000, 1):
            mywriter = csv.writer(csvfile, delimiter=',')
            prd_id = f"prd{str(count).zfill(5)}"
            desc = random_string(random.randint(1,15))
            prod_type = random_string(random.randint(1,15))
            quantity = random.randint(1,10)

            mywriter.writerow([prd_id, desc, prod_type, quantity])
            count += 1


def random_customers(directory_name, customer_file):
    file_name = directory_name + customer_file
    count = 3
    with open(file_name, 'a', newline='') as csvfile:
        for i in range(0, 1000, 1):
            mywriter = csv.writer(csvfile, delimiter=',')
            user_id = f"user{str(count).zfill(5)}"
            name = random_string(random.randint(1,15))
            address = random_string(random.randint(1,15))
            phone = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            email = f"{random_string(random.randint(1,15))}@email.com"

            mywriter.writerow([user_id, name, address, phone, email])
            count += 1


def random_rentals(directory_name, rental_file):
    file_name = directory_name + rental_file
    count = 3
    with open(file_name, 'a', newline='') as csvfile:
        for i in range(0, 1000, 1):
            mywriter = csv.writer(csvfile, delimiter=',')
            rnt_id = f"rnt{str(count).zfill(5)}"
            user_id = f"user{str(random.randint(1,1000)).zfill(5)}"
            prd_id = f"prd{str(random.randint(1,1000)).zfill(5)}"

            mywriter.writerow([rnt_id, user_id, prd_id])
            count += 1


if __name__ == '__main__':
    random_products("./", "products.csv")
    random_customers("./", "customers.csv")
    random_rentals("./", "rentals.csv")
