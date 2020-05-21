import csv
import pandas as pd
import functools


def add_furniture(invoice_file,
                  customer_name,
                  item_code,
                  item_description,
                  item_monthly_price):
    with open(invoice_file, "a+", newline="") as f:
        add_line = [customer_name, item_code, item_description, item_monthly_price]
        writer = csv.writer(f, delimiter=",")
        writer.writerow(add_line)


def single_customer(customer_name,
                    invoice_file):
    def adder(rental_items):
        with open(rental_items, "r") as file:
            data = pd.read_csv(file)
            partial = functools.partial(add_furniture,
                                        invoice_file=invoice_file,
                                        customer_name=customer_name)
            for line in data.to_dict("records"):
                item_code, item_description, item_monthly_price = line.values()
                partial(item_code=item_code,
                        item_description=item_description,
                        item_monthly_price=item_monthly_price)
    return adder

