# pylint: disable=invalid-name
"""Generate CSV files with sample data"""
import csv
from random import randrange


def main():
    """Generate CSV files with sample data"""
    # number of rows to generate in each file
    rowcount = 10000

    # build customers csv
    with open('data/customers.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["customer_id",
                         "name",
                         "address",
                         "phone_number",
                         "email"])

        for i in range(rowcount):
            row = [f"user{i+1:03d}",
                   "John Doe",
                   "123 Example Street",
                   "15551234567",
                   "john@example.com"]
            writer.writerow(row)

    # build products csv
    with open('data/products.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["product_id",
                         "description",
                         "product_type",
                         "quantity_available"])

        for i in range(rowcount):
            row = [f"prd{i+1:03d}",
                   "Generic Object",
                   "randcat",
                   randrange(1, 99)]
            writer.writerow(row)

    # build rentals csv
    with open('data/rentals.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["rental_id", "customer_id", "product_id"])

        for i in range(rowcount):
            row = [f"rnt{i+1:03d}",
                   f"user{randrange(1,999):03d}",
                   f"prd{randrange(1,999):03d}"]
            writer.writerow(row)


if __name__ == "__main__":
    main()
