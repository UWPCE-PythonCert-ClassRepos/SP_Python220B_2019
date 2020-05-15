#!/usr/bin/env python3
# pylint: disable=R0913,R0903,W0603
'''launches the user interface for the inventory management system'''

import sys
import market_prices as mp
import inventory_class as ic
import furniture_class as fc
import electric_appliances_class as eac


def main_menu(user_prompt=None):
    '''some stuff12'''
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"please choose from the following options ({options_str}):")
        print("1. add a new item to the inventory")
        print("2. get item information")
        print("q. quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price(item_code):
    '''some stuff13'''
    return(f"get price for {item_code}")


def add_new_item():
    '''some stuff14'''
    global FULL_INVENTORY
    item_code = input("enter item code: ")
    item_description = input("enter item description: ")
    item_rental_price = input("enter item rental price: ")

    # get price from the market prices module
    item_price = mp.get_latest_price(item_code)

    isfurniture = input("is this item a piece of furniture? (y/n): ")
    if isfurniture.lower() == "y":
        item_material = input("enter item material: ")
        itemsize = input("enter item size (s, m, l, xl): ")
        newitem = fc.Furniture(item_code, item_description,
                               item_price, item_rental_price,
                               item_material, itemsize)
    else:
        iselectricappliance = input("is this item an electric appliance? (y/n): ")
        if iselectricappliance.lower() == "y":
            item_brand = input("enter item brand: ")
            itemvoltage = input("enter item voltage: ")
            newitem = eac.ElectricAppliances(item_code,
                                             item_description,
                                             item_price,
                                             item_rental_price,
                                             item_brand,
                                             itemvoltage)
        else:
            newitem = ic.Inventory(item_code, item_description,
                                   item_price, item_rental_price)
    FULL_INVENTORY[item_code] = newitem.return_as_dictionary()
    print("new inventory item added")


def item_info():
    '''some stuff15'''
    item_code = input("enter item code: ")
    if item_code in FULL_INVENTORY:
        printdict = FULL_INVENTORY[item_code]
        for k, value in printdict.items():
            print("{}:{}".format(k, value))
    else:
        print("item not found in inventory")


def exit_program():
    '''quit the program'''
    sys.exit()


if __name__ == '__main__':
    FULL_INVENTORY = {}
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("press enter to continue...........")
