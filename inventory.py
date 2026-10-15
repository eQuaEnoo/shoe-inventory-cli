"""
Shoe inventory management system.

A menu-driven command-line program that loads shoe stock records from
inventory.txt, models each shoe as a Shoe object, and lets the user view,
add, search, and restock items. Changes are saved back to inventory.txt.

Usage:
    python inventory.py
"""

import csv
from pathlib import Path

# The inventory file lives next to this script, so the program operates no
# matter which directory it is launched from.
INVENTORY_PATH = Path(__file__).resolve().parent / "inventory.txt"
HEADER = ["Country", "Code", "Product", "Cost", "Quantity"]
CURRENCY = "R"


# ======================== Shoe class ========================
class Shoe:
    """A single shoe line item in the inventory."""

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """Return the cost of one pair of shoes."""
        return self.cost

    def get_quantity(self):
        """Return the number of pairs in stock."""
        return self.quantity

    def __str__(self):
        return (f"Country:  {self.country}\n"
                f"Code:     {self.code}\n"
                f"Product:  {self.product}\n"
                f"Cost:     {CURRENCY}{self.cost:.2f}\n"
                f"Quantity: {self.quantity}")


# In-memory list of Shoe objects, filled by read_shoes_data().
shoes_list = []


# ==========File handling==============
def read_shoes_data():
    """Load inventory.txt into shoes_list."""
    shoes_list.clear()  # avoids duplicates if this is ever called twice
    try:
        with INVENTORY_PATH.open("r", newline="") as file:
            reader = csv.reader(file, skipinitialspace=True)
            next(reader, None)  # skip the header row
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue  # ignore blank lines
                try:
                    country, code, product, cost, quantity = row
                    shoes_list.append(
                        Shoe(country, code, product, cost, quantity)
                    )
                except ValueError:
                    print(f"Skipping malformed line {line_number}: {row}")
        print(f"\n{len(shoes_list)} shoes loaded from the inventory.\n")
    except FileNotFoundError:
        print(f"Could not find {INVENTORY_PATH}. Please check the path.\n")
    except OSError as error:
        print(f"Could not read the inventory file: {error}\n")


def write_to_file():
    """Overwrite inventory.txt with the current contents of shoes_list."""
    try:
        with INVENTORY_PATH.open("w", newline="") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(HEADER)
            for shoe in shoes_list:
                writer.writerow(
                    [shoe.country, shoe.code, shoe.product,
                     shoe.cost, shoe.quantity]
                )
    except OSError as error:
        print(f"\nFailed to update inventory file: {error}\n")


# ======================== Helpers ========================
def find_shoe(code):
    """Return the Shoe with this code (case-insensitive), or None."""
    for shoe in shoes_list:
        if shoe.code.upper() == code.upper():
            return shoe
    return None


# ======================== Menu actions ========================
def capture_shoes():
    """Prompt for a new shoe's details save the it."""
    print("\n---- Add New Shoe ----")
    country = input("Country: ").strip()
    code = input("Code (e.g. SKU12345): ").strip()
    product = input("Product: ").strip()

    if find_shoe(code):
        print(f"\nA shoe with code '{code}' already exists. Not added.\n")
        return

    try:
        cost = float(input(f"Cost ({CURRENCY}): ").strip())
        quantity = int(input("Quantity: ").strip())
    except ValueError:
        print("\nCost and quantity must be numbers. Shoe not added.\n")
        return

    if cost < 0 or quantity < 0:
        print("\nCost and quantity must be non-negative. Shoe not added.\n")
        return

    shoes_list.append(Shoe(country, code, product, cost, quantity))
    write_to_file()  # Write the updated shoes_list to inventory.txt
    print(f"\n'{product}' added successfully.\n")


def view_all():
    """Print the details of every shoe in stock."""
    if not shoes_list:
        print("\nNo shoes in inventory.\n")
        return

    print("\n---- Shoe Inventory ----")
    for number, shoe in enumerate(shoes_list, start=1):
        print(f"\n[{number}]")
        print(shoe)
        print("-" * 40)


def re_stock():
    """Offer to restock the shoe with the lowest quantity."""
    if not shoes_list:
        print("\nNo shoes in inventory to restock.\n")
        return

    # Find the shoe with the lowest quantity
    lowest = min(shoes_list, key=lambda shoe: shoe.get_quantity())
    print("\n---- Restock Alert ----\n")
    print(f"Lowest stock: {lowest.product}, "
          f"{lowest.get_quantity()} units left")

    answer = input(
        "Would you like to restock this item? (yes/no): ").strip().lower()
    if answer != "yes":
        print("Restock cancelled.\n")
        return

    try:
        add_quantity = int(input("How many units to add? ").strip())
    except ValueError:
        print("Please enter a whole number.\n")
        return

    if add_quantity <= 0:
        print("Please enter a number greater than 0.\n")
        return

    lowest.quantity += add_quantity
    write_to_file()  # Save the updated quantity to inventory.txt
    print(f"\n{lowest.product} restocked.\n"
          f"New quantity: {lowest.get_quantity()} units.\n")


def search_shoe():
    """Look up a shoe by its product code and displays it."""
    print("\n---- Search Shoe by Code ----")
    code = input("Enter shoe code: ").strip()
    shoe = find_shoe(code)

    if shoe:
        print("\nShoe found:\n")
        print(shoe)
        print()
    else:
        print(f"\nNo shoe found with code '{code}'.\n")


def value_per_item():
    """Print the total stock value (cost * quantity) of each shoe."""
    if not shoes_list:
        print("\nNo shoes available.\n")
        return

    print("\n---- Value per Item ----")
    print(f"{'Product':<25} {'Cost':>10} {'Quantity':>9} {'Total Value':>14}")
    print("-" * 61)

    for shoe in shoes_list:
        # Attach the currency symbol to the values before aligning so
        # the "R" symbol stays attached to the digits instead of floating
        # in the padding.
        cost = f"{CURRENCY}{shoe.get_cost():.2f}"
        value = f"{CURRENCY}{shoe.get_cost() * shoe.get_quantity():.2f}"

        print(f"{shoe.product:<25} "
              f"{cost:>10} "
              f"{shoe.get_quantity():>9} "
              f"{value:>14}")
    print()


def highest_qty():
    """Show the best-stocked shoe, flagged as the item on sale."""
    if not shoes_list:
        print("\nNo shoes loaded.\n")
        return

    highest = max(shoes_list, key=lambda shoe: shoe.get_quantity())
    print("\n---- Highest Stock Item ----\n")
    print(f"ON SALE:    {highest.product}")
    print(f"Code:       {highest.code}")
    print(f"Quantity:   {highest.get_quantity()} units\n")


# ======================== Main menu ========================
MENU = """
---- Shoe Inventory System ----
1. View all shoes
2. Add a new shoe
3. Restock lowest item
4. Search by code
5. Value per item
6. Highest quantity item
0. Exit
"""

# Maps each menu choice to the function that handles it.
ACTIONS = {
    "1": view_all,
    "2": capture_shoes,
    "3": re_stock,
    "4": search_shoe,
    "5": value_per_item,
    "6": highest_qty,
}


def main_menu():
    """Load the data, then loop through the menu until the user exits."""
    read_shoes_data()

    while True:
        print(MENU)
        choice = input("Select an option: ").strip()

        if choice == "0":
            print("Exiting the program. Goodbye!")
            break

        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please choose from the menu.\n")


if __name__ == "__main__":
    main_menu()
