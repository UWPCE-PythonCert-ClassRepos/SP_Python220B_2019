'''launches the user interface for the inventory management system'''
import sys
import market_prices
import inventory_class
import furniture_class
import electric_appliances_class


def mainmenu(user_prompt=None):
    '''some stuff12'''
    valid_prompts = {"1": addnewitem,
                     "2": iteminfo,
                     "q": exitprogram}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"please choose from the following options ({options_str}):")
        print("1. add a new item to the inventory")
        print("2. get item information")
        print("q. quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def getprice(item_code):
    '''some stuff13'''
    print("get price")


def addnewitem():
    '''some stuff14'''
    global FULLINVENTORY
    item_code = input("enter item code: ")
    item_description = input("enter item description: ")
    item_rental_price = input("enter item rental price: ")

    # get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    isfurniture = input("is this item a piece of furniture? (y/n): ")
    if isfurniture.lower() == "y":
        item_material = input("enter item material: ")
        itemsize = input("enter item size (s, m, l, xl): ")
        newitem = furniture_class.Furniture(item_code, item_description,
                                            item_price, item_rental_price,
                                            item_material, itemsize)
    else:
        iselectricappliance = input("is this item an electric appliance? (y/n): ")
        if iselectricappliance.lower() == "y":
            item_brand = input("enter item brand: ")
            itemvoltage = input("enter item voltage: ")
            newitem = electric_appliances_class.ElectricAppliances(item_code,
                                                                   item_description,
                                                                   item_price,
                                                                   item_rental_price,
                                                                   item_brand,
                                                                   itemvoltage)
        else:
            newitem = inventory_class.Inventory(item_code, item_description,
                                                item_price, item_rental_price)
    FULLINVENTORY[item_code] = newitem.return_as_dictionary()
    print("new inventory item added")


def iteminfo():
    '''some stuff15'''
    item_code = input("enter item code: ")
    if item_code in FULLINVENTORY:
        printdict = FULLINVENTORY[item_code]
        for k, value in printdict.items():
            print("{}:{}".format(k, value))
    else:
        print("item not found in inventory")


def exitprogram():
    '''some stuff16'''
    sys.exit()


if __name__ == '__main__':
    '''some stuff17'''
    FULLINVENTORY = {}
    while True:
        print(FULLINVENTORY)
        mainmenu()()
        input("press enter to continue...........")
