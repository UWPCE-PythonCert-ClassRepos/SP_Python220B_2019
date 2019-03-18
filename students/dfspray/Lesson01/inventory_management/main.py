"""Launches the user interface for the inventory management system"""
import sys
import inventory_management.market_prices as market_prices
import inventory_management.inventory_class as inventory_class
import inventory_management.furniture_class as furniture_class
import inventory_management.electric_appliances_class as electric_appliances_class

def main_menu(user_prompt=None):
    """Displays an input menu"""
    valid_prompts = {"1": add_new_item,
                     "2": item_info,
                     "q": exit_program}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (",  {}") * (len(options)-1)).format(*options)
        print(f"Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

def get_price(item_code):
    """Creates a method to print 'Get Price'"""
    print("Get price")
    return market_prices.get_latest_price(item_code)

def add_new_item():
    """Creates a method to add a new item"""
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    inventory_info = [item_code, item_description, item_price, item_rental_price]

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S, M, L, XL): ")
        new_item = furniture_class.Furniture(
            inventory_info,
            item_material,
            item_size
        )
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = electric_appliances_class.ElectricAppliances(
                inventory_info,
                item_brand,
                item_voltage
            )
        else:
            new_item = inventory_class.Inventory(
                inventory_info
            )
    FULL_INVENTORY[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def item_info():
    """Creates a method to get information on an item"""
    item_code = input("Enter item code: ")
    if item_code in FULL_INVENTORY:
        print_dict = FULL_INVENTORY[item_code]
        output_list = []
        for code, item in print_dict.items():
            print("{}:{}".format(code, item))
            output_list.append("{}:{}".format(code, item))
        output_message = '\n'.join(output_list)
    else:
        output_message = "Item not found in inventory"
        print(output_message)
    return output_message

def exit_program():
    """Creates a method to exit the program"""
    sys.exit()

def return_full_inventory():
    """Creates a method to return the full inventory of items"""
    return FULL_INVENTORY

FULL_INVENTORY = {}

if __name__ == '__main__':
    while True:
        print(FULL_INVENTORY)
        main_menu()()
        input("Press Enter to continue...........")
