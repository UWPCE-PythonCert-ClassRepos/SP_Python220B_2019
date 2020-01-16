""" Launches the user interface for the inventory management system """

import sys
import market_prices
import inventoryclass
import furnitureclass
import electricappliancesclass

FULLINVENTORY = {}

def mainmenu(user_prompt=None):
    """ User interface to the inventory application """
    valid_prompts = {"1": addnewitem,
                     "2": iteminfo,
                     "q": exitprogram}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        _options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options ({_options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def getprice():
    """ Prints the price of item """
    print("Get price")


def addnewitem():
    """ Adds new item into inventory """
    global FULL_INVENTORY
    itemcode = input("Enter item code: ")
    itemdescription = input("Enter item description: ")
    itemrentalprice = input("Enter item rental price: ")

    # Get price from the market prices module
    itemprice = market_prices.get_latest_price(itemcode)

    isfurniture = input("Is this item a piece of furniture? (Y/N): ")
    if isfurniture.lower() == "y":
        itemmaterial = input("Enter item material: ")
        itemsize = input("Enter item size (S, M, L, XL): ")
        newitem = furnitureclass.Furniture(itemmaterial, itemsize, itemcode,
                                           itemdescription,
                                           itemprice,
                                           itemrentalprice)
    else:
        iselectricappliance = input("Is this item an electric appliance? (Y/N): ")
        if iselectricappliance.lower() == "y":
            itembrand = input("Enter item brand: ")
            itemvoltage = input("Enter item voltage: ")
            newitem = electricappliancesclass.ElectricAppliances(itembrand,
                                                                 itemvoltage,
                                                                 itemcode,
                                                                 itemdescription,
                                                                 itemprice,
                                                                 itemrentalprice)
        else:
            newitem = inventoryclass.Inventory(itemcode, itemdescription,

                                               itemprice, itemrentalprice)
    FULLINVENTORY[itemcode] = newitem.return_as_dictionary()
    print("New inventory item added")


def iteminfo():
    """ Retrieves the attributes of the item by item code """
    itemcode = input("Enter item code: ")
    if itemcode in FULLINVENTORY:
        printdict = FULLINVENTORY[itemcode]
        for k, value in printdict.items():
            print("{}:{}".format(k, value))
    else:
        print("Item not found in inventory")


def exitprogram():
    """ Exits the system gracefully """
    sys.exit()


if __name__ == '__main__':
    FULLINVENTORY = {}
    while True:
        print(FULLINVENTORY)
        mainmenu()()
        input("Press Enter to continue...........")
