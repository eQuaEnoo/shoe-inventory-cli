# Shoe Inventory System

A command-line inventory management program built in Python. The system 
loads shoe stock records from `inventory.txt`, models each shoe as a 
`Shoe` object, and lets the user view, add, search, and manage stock 
through a menu-driven interface.

## Features

- **View all shoes** — displays full details for every shoe in stock
- **Add a new shoe** — captures country, code, product, cost, and quantity, 
  with input validation for cost and quantity
- **Restock lowest item** — automatically identifies the shoe with the lowest 
  quantity and prompts the user to add stock
- **Search by code** — looks up a shoe using its unique product code
- **Value per item** — calculates and displays the total stock value 
  (cost × quantity) for each shoe
- **Highest quantity item** — identifies the best-stocked shoe, flagged as 
  the item currently on sale

## How it works

Shoe data is stored in `inventory.txt` in CSV format (`Country,Code,Product,Cost,Quantity`), 
one shoe per line. On startup, the program reads this file and builds a list of 
`Shoe` objects in memory. Changes made during a session (adding stock or 
restocking) are written back to `inventory.txt` so the file stays in sync 
with the program state.

## Usage

Clone the repository and run the script:

```bash
git clone https://github.com/eQuaEnoo/shoe-inventory-cli.git
cd shoe-inventory-cli
python inventory.py
```

Then choose an option from the menu (0–6) to interact with the inventory.

## Requirements

- Python 3
- `inventory.txt` must be present in the same directory as `inventory.py`
