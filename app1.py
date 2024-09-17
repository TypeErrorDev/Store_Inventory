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
    print(split_date)
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
            \n******* DATE ERROR *******
            \rIncorrect date format. Date should look like: 
            \rEx: MM/DD/YYYY
            \rPress enter to try again.
            \r**************************''')     
        return       
    else:
        return return_date
    


def clean_price(price_str):
    try:
        # Remove currency symbols and commas
        price_str = price_str.replace('$', '').replace(',', '')
        
        # Convert to float
        price_float = float(price_str)
        
        # Convert to cents (if needed)
        return int(round(price_float * 100))
    except ValueError:
        input('''
            \n******* PRICE ERROR *******
            \rThe price format should be numerical with no currency sign: 
            \rEx: 5.99
            \rPress enter to try again.
            \r**************************''')     
        return 



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
    products_to_add = []
    try:
        with open('inventory.csv', newline='') as inventory_csv:
            reader = csv.reader(inventory_csv)
            next(reader)  # Skip the header row

            existing_brand_names = set(brand.brand_name for brand in existing_brands)
            
            existing_products = {
                (product.product_name, product.brand_id): product
                for product in session.query(Products).all()
            }

            for row in reader:
                product_name = row[0]
                product_price = float(clean_price(row[1]))
                product_quantity = int(row[2])
                date_updated = clean_date(row[3])
                brand_name = row[4]

                if brand_name not in existing_brand_names:
                        print(f"Warning: Brand '{brand_name}' not found in the database. Skipping product '{product_name}'.")
                        continue

                brand = session.query(Brands).filter_by(brand_name=brand_name).first()
            
                if not brand:
                    print(f"Warning: Brand '{brand_name}' not found in the database. Skipping product '{product_name}'.")
                    continue

                product_key = (product_name, brand.brand_id)
            
                if product_key not in existing_products:
                    new_product = Products(
                        product_name=product_name,
                        product_price=product_price,
                        product_quantity=product_quantity,
                        date_updated=date_updated,
                        brand_id=brand.brand_id
                    )
                    products_to_add.append(new_product)
                    products_added += 1
        
        if products_to_add:
            session.add_all(products_to_add)
            session.commit()
            print(f"Added {products_added} products from inventory.csv")
    except FileNotFoundError:
        print("inventory.csv file not found.")
    except Exception as e:
        print(f"Error processing inventory.csv: {e}")

def app():
    app_running = True
    
    while app_running:
        choice = menu()
        
        if choice == 'v':
            # View a single product's inventory 
            pass
        elif choice == 'n':
            # Add a new product to the database
            product_name=input("Product Name: ")
            price_error = True
            while price_error:         
                product_price=input("Price (Ex: $5.06): ")
                product_price=clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            product_quantity=input("Quantity: ")
            date_error = True
            while date_error:
                date_updated=input("Date Updated (Ex: 3/9/2019): ")
                date_updated=clean_date(date_updated)
                if type(date_updated) == datetime.date:
                    date_error = False
            
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
    app()


