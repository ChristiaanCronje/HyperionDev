import os

# Defines a Shoe class with country, code, product, cost and quantity
# Attributes. It includes a method to get the cost and another to get 
# The quantity of the shoe. It also includes a string method which 
# Returns all the attributes.
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return (
            f"Product: {self.product}, "
            f"Code: {self.code}, "
            f"Country: {self.country}, "
            f"Cost: R{self.cost}.00, "
            f"Quantity: {self.quantity}"
        )

shoe_list = []

# Extract all the shoe data inside "inventory.txt" where each line 
# Creates one Shoe object and stores it inside the shoe list.
def read_shoes_data():
    shoe_list.clear()

    try:
        with open('inventory.txt', 'r') as inventory_file:
            inventory = inventory_file.readlines()

        for shoe_details in inventory[1:]:
            shoe_data = shoe_details.strip()
            shoe_data = shoe_data.split(',')
            shoe = Shoe(
                shoe_data[0], 
                shoe_data[1], 
                shoe_data[2], 
                int(shoe_data[3]), 
                int(shoe_data[4])
            )
            shoe_list.append(shoe)
        
        print('\nData read successfully!')

    except FileNotFoundError:
        print('\nThe file "inventory.txt" was not found.')

    except ValueError as error:
        print(
            "\nInvalid data format in 'inventory.txt'. "
            "Please check that all cost and quantity values are numeric."
        )
        print(f"Details: {error}")


# Request shoe detail input from the user to create another shoe object
# And add it to the shoe list. It then appends the shoe object to 
# "Inventory.txt"
def capture_shoes():
    country = input("Please input the country that the shoe is produced in: ")

    if not country:
        print('\nCountry cannot be empty.')
        return

    code = input("Please input the code: ")

    if not code:
        print('\nCode cannot be empty.')
        return
    
    if not (code[:3] == 'SKU' and len(code[3:]) == 5 and code[3:].isdigit()):
        print('\nCode must start with "SKU" and end with 5 digits only.')
        return
    
    for shoe in shoe_list:
        if shoe.code == code:
            print("\nThis shoe code already exists. Please use a unique code.")
            return
    
    product = input("Please input the product name: ")

    if not product:
        print('\nProduct name cannot be empty.')
        return

    try:
        cost = int(input("Please input the cost: "))

        if cost <= 0:
            print('\nCost must be a positive number.')
            return
        
        quantity = int(input("Please input the quantity: "))

        if quantity < 0:
            print('\nQuantity cannot be negative.')
            return
    
    except ValueError:
        print('\nPlease enter valid numerical values.')
        return

    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)

    file_exists = os.path.isfile("inventory.txt")

    with open("inventory.txt", "a") as inventory_file:
        if not file_exists:
            inventory_file.write('Country,Code,Product,Cost,Quantity\n')

        inventory_file.write(
            f"{shoe.country},"
            f"{shoe.code},"
            f"{shoe.product},"
            f"{shoe.cost},"
            f"{shoe.quantity}\n"
        )

    print('\nNew shoe added successfully!')


# Prints out the shoe details of each shoe in the shoe list.
def view_all():
    if shoe_list:
        for shoe in shoe_list:
            print(shoe)

    else:
        print("Please first read the shoe data.")


# Finds the shoe lowest in quantity in the shoe list, then asks how much
# Stock the user wants to add. It updates the new quantity value to
# "Inventory.txt" and shoe list.
def re_stock():
    if not shoe_list:
        print("Please first read the shoe data.")
        return
    
    lowest_quantity_shoe = shoe_list[0]

    for shoe in shoe_list[1:]:
        if shoe.get_quantity() < lowest_quantity_shoe.get_quantity():
            lowest_quantity_shoe = shoe

    print(
        f'The shoe with the lowest stock is: {lowest_quantity_shoe.product}. ' 
        f'We have {lowest_quantity_shoe.get_quantity()} in stock.\n'
    )

    try:
        add_quantity_amount = int(input('How much do you want to add? '))

        if add_quantity_amount <= 0:
            print("\nPlease enter a positive number.")
            return

    except ValueError:
        print("Please enter a numerical value.")
        return

    lowest_quantity_shoe.quantity += add_quantity_amount

    with open('inventory.txt', 'w') as inventory_file:
        inventory_file.write('Country,Code,Product,Cost,Quantity\n')

        for shoe in shoe_list:
            inventory_file.write(
                f'{shoe.country},'
                f'{shoe.code},'
                f'{shoe.product},'
                f'{shoe.cost},'
                f'{shoe.quantity}\n'
            )

    print('\nStock updated!')
            

# Request the user to input a shoe code. If the code matches a shoe code
# In the shoe list, it will display the data of that shoe product.
def search_shoe():
    if not shoe_list:
        return "\nPlease first read the shoe data."
    
    shoe_code = input('\nPlease enter the shoe code: ')

    for shoe in shoe_list:
        if shoe_code == shoe.code:
            return shoe
    
    return '\nInvalid shoe code.'


# Prints out the total value of each shoe product in the shoe list.
def value_per_item():
    if not shoe_list:
        print("Please first read the shoe data.")
        return
    
    for shoe in shoe_list:
        shoe_total_value = shoe.get_cost()*shoe.get_quantity()
        print(f'{shoe.product}: R{shoe_total_value}.00')


# Finds the shoe highest in quantity in the shoe list then displays that
# The shoe product is for sale.
def highest_qty():
    if not shoe_list:
        print("Please first read the shoe data.")
        return
    
    highest_quantity_shoe = shoe_list[0]

    for shoe in shoe_list[1:]:
        if shoe.get_quantity() > highest_quantity_shoe.get_quantity():
            highest_quantity_shoe = shoe
    
    print(
        f'{highest_quantity_shoe.product} is for sale. '
        f'We have {highest_quantity_shoe.get_quantity()} in stock.'
    )

while True:
    choice = input("""Do you want to: 
r - read shoes data from the textfile
a - add a new shoe to the list
va - view all the shoe details
rs - restock the lowest quantity shoe
s - search for a spesific shoe
dv - display the value for each shoe
dh - display the highest quantity shoe is for sale
e - exit the program
""").lower()
    
    if choice == 'r':
        read_shoes_data()
        print()

    elif choice == 'a':
        print()
        capture_shoes()
        print()

    elif choice == 'va':
        print()
        view_all()
        print()

    elif choice == 'rs':
        print()
        re_stock()
        print()

    elif choice == 's':
        print()
        print(search_shoe())
        print()

    elif choice == 'dv':
        print()
        value_per_item()
        print()

    elif choice == 'dh':
        print()
        highest_qty()
        print()

    elif choice == 'e':
        break

    else:
        print('\nPlease pick a choice from the menu.\n')

print()