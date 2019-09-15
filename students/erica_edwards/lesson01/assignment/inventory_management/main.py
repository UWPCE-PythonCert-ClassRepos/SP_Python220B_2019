#!/usr/bin/env python3
"""Launches the user interface for the inventory management system"""

import sys
import market_prices
import inventory_class
import furniture_class
import electric_appliances_class
# import inventory_management.market_prices as market_prices
# import inventory_management.inventory_class as inventory_class
# import inventory_management.furniture_class as furniture_class
# import inventory_management.electric_appliances_class as electric_appliances_class

# pylint: disable=W0612, W0603, C0103
FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    """Main Menu"""
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


# def get_price(item_code):
#     """Get the price"""
#     print("Get price")


def add_new_item():
    """Add new item to inventory"""
    global FULL_INVENTORY
    item_code = input("Enter item code: ")
    print(item_code)
    item_description = input("Enter item description: ")
    print(item_description)
    item_rental_price = input("Enter item rental price: ")
    print(item_rental_price)
    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    print(is_furniture)
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        print(item_material)
        item_size = input("Enter item size (S,M,L,XL): ")
        print(item_size)
        new_item = furniture_class.Furniture(item_code, item_description, item_price,
                                             item_rental_price, item_material, item_size)
        print(new_item.return_as_dictionary())
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            print(item_brand)
            item_voltage = input("Enter item voltage: ")
            print(item_voltage)
            new_item = electric_appliances_class.ElectricAppliances(item_code, item_description,
                                                                    item_price, item_rental_price,
                                                                    item_brand, item_voltage)
            print(new_item.return_as_dictionary())
        else:
            new_item = inventory_class.Inventory(item_code, item_description, item_price,
                                                 item_rental_price)
        print(new_item.return_as_dictionary())
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """Get item information"""
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for k, v in print_dict.items():
            print("{}:{}".format(k, v))
    else:
        print("Item not found in inventory")


def exit_program():
    """Exit"""
    sys.exit()


if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
