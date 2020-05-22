"""
This module launches the user interface for the inventory management system
"""
import sys

from inventory_management.market_prices import get_latest_price
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances


FULL_INVENTORY = []


def main_menu(user_prompt=None):
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options) - 1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        # print("Please choose from the following options:")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

# def get_price(item_code):
#    print("Get price")


def add_new_item():
    # global FULL_INVENTORY
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = get_latest_price(item_code)
    new_item_dict = {'product_code': item_code,
                     'description': item_description,
                     'market_price': item_price,
                     'rental_price': item_rental_price
                     }

    is_furniture = input("Is this item a piece of Furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = Furniture(material=item_material, size=item_size,
                             **new_item_dict)
    else:
        is_electric_appliance = input("Is this item an electric appliance? \
(Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = ElectricAppliances(brand=item_brand,
                                          voltage=item_voltage,
                                          **new_item_dict)
        else:
            new_item = Inventory(**new_item_dict)
    FULL_INVENTORY.append(new_item)
    print("New inventory item added")


def item_info():
    item_code = input("Enter item code: ")
    # filter() returns an iterator that pass the function check,
    # so we can use next() to get these items.
    found_it = next(filter(lambda x: x.product_code == item_code,
                           FULL_INVENTORY), None)

    if found_it is not None:
        print(found_it)
    else:
        print("Item not found in inventory")


def exit_program():
    sys.exit()


if __name__ == '__main__':
    while True:
        # for item in FULL_INVENTORY:
        #   print(item)
        main_menu()()
        input("Press Enter to continue...........")
