from inventory import add_furniture, single_customer

if __name__ == "__main__":

    add_furniture("rented_items.csv", "Elisa Miles", "LR04",
                  "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data", "KT78",
                  "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales", "KFC12",
                  "Queen Mattress", 17)

    create_invoice = single_customer("Sifu Wong", "rented_items.csv")
    create_invoice("test_items.csv")

    create_invoice = single_customer("Ween Wong", "rented_items.csv")
    create_invoice("test_items.csv")
