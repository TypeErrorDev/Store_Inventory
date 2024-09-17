from models import Base, session, Products, Brands, engine
import datetime
import csv
from decimal import Decimal


def menu():
    while True:
        print('''
            \n    ****** INVENTORY MENU ******
              \nV) View a single product's inventory 
              \rN) Add a new product to the database
              \rA) View an analysis of the inventory
              \rB) Make a backup of the entire inventory
              \rX) Exit the program''')
        choice = input('\nWhat would you like to do? ').lower().strip()
        if choice in ['v', 'n', 'a', 'b', 'x']:
            return choice
        else:
            input('''\n***** ERROR *****
                  \nPlease choose one of the options above.
                  \rPress enter to try again''')


# add - add a new record
# edit books
# delete books
# search - search for a book
# data cleaning - remove duplicates

def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])  # No need for months.index() + 1
    day = int(split_date[1])
    year = int(split_date[2])
    return datetime.date(year, month, day)


def clean_price(price_str):   
    return Decimal(price_str.replace('$', ''))


def add_brands_from_csv():
    brands_added = set()
    with open('brands.csv', newline='') as brands_csv:
        reader = csv.reader(brands_csv)
        next(reader)  # Skip the header row
        for row in reader:
            brand_name = row[0]
            if brand_name not in brands_added:
                brand = session.query(Brands).filter_by(brand_name=brand_name).first()
                if not brand:
                    brand = Brands(brand_name=brand_name)
                    session.add(brand)
                    brands_added.add(brand_name)
    session.commit()
    print(f"Added {len(brands_added)} brands from brands.csv")
    return brands_added


def add_inventory_from_csv(existing_brands):
    products_added = 0
    with open('inventory.csv', newline='') as inventory_csv:
        reader = csv.reader(inventory_csv)
        next(reader)  # Skip the header row
        for row in reader:
            product_name = row[0]
            product_price = float(clean_price(row[1]))
            product_quantity = int(row[2])
            date_updated = clean_date(row[3])
            brand_name = row[4]

            brand = session.query(Brands).filter_by(brand_name=brand_name).first()
            if not brand:
                print(f"Warning: Brand '{brand_name}' not found in the database. Skipping product '{product_name}'.")
                continue

            new_product = Products(
                product_name=product_name,
                product_price=product_price,
                product_quantity=product_quantity,
                date_updated=date_updated,
                brand_id=brand.brand_id
            )
            session.add(new_product)
            products_added += 1

    session.commit()
    print(f"Added {products_added} products from inventory.csv")

# def add_csv():
#     brands_added = set()

#     with open('brands.csv') as brands_csv:
#         data = csv.reader(brands_csv)
#         for row in data:
#             brand_name =row[0]
#             print(row)

#     with open('inventory.csv') as inventory_csv:
#         data = csv.reader(inventory_csv)
#         for row in data:
#             product_name = row[0]
#             product_price = clean_price(row[1])
#             product_quantity = row[2]
#             date_updated = clean_date(row[3])
#             brand_name = row[4]
#             new_product = Products(product_name=product_name,product_quantity=product_quantity,date_updated=date_updated,brand_name=brand_name)
#             session.add(new_product)
#         print(row)
#         session.commit()
            

def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            # View a single product's inventory 
            pass
        elif choice == 'n':
            # Add a new product to the database
            pass
        elif choice == 'a':
            # View an analysis of the inventory
            pass
        elif choice == 'b':
            # Create a backup of the inventory
            pass
        else:
            print('GOODBYE FRIENDS!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    existing_brands = add_brands_from_csv()
    add_inventory_from_csv(existing_brands)

    for product in session.query(Products).join(Brands):
        print(f"Product: {product.product_name}, Brand: {product.brand.brand_name}, "
              f"Price: ${product.product_price:.2f}, Quantity: {product.product_quantity}")


