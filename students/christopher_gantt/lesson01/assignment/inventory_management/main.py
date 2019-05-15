'''Launches the user interface for the inventory management system'''
# .pylintrc disable = useless-import-alias

import sys
import inventory_management.market_prices as market_prices
import inventory_management.inventory_class as inventory_class
import inventory_management.furniture_class as furniture_class
import inventory_management.electric_appliances_class as electric_appliances_class

FULL_INVENTORY = {}

def main_menu(user_prompt=None):
    """function creates the main menu and asks for a selection"""
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        option_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({option_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)


def get_price(item_code):
    '''returns the latest market price from the market_prices module'''
    return market_prices.get_latest_price(item_code)


def add_new_item():
    '''adds a new item to the inventory'''
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = furniture_class.Furniture(item_code,
                                             item_description,
                                             item_price,
                                             item_rental_price,
                                             item_material,
                                             item_size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(item_code,
                                                                    item_description,
                                                                    item_price,
                                                                    item_rental_price,
                                                                    item_brand,
                                                                    item_voltage)
        else:
            new_item = inventory_class.Inventory(item_code,
                                                 item_description,
                                                 item_price,
                                                 item_rental_price)
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    '''returns the items information'''
    item_code = input("Enter item code: ")
    info_list = []
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        for key, value in print_dict.items():
            info_list.append("{}:{}".format(key, value))
        info = '\n'.join(info_list)
        print(info)
    else:
        info = "Item not found in inventory"
        print(info)
    return info


def return_full_inventory():
    '''returns the full inventory dict'''
    return FULL_INVENTORY


def exit_program():
    '''quits the program, accessed from the main menu'''
    sys.exit()


if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        # Consider adding an option to show full inventory.
        # Seeing the full inventory after every new item added or item information
        # requested would be very odd when running the program.
        main_menu()()
        input("Press Enter to continue...........")
