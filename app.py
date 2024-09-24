from models import Base, session, Products, Brands, engine
from datetime import datetime
from sqlalchemy import select, func
import csv
import time


def menu():
    while True:
        print('''
            \n****** Inventory Menu ******
            \nV) View a single product's inventory
            \rN) Add a new product to the database
            \rA) View the analysis options
            \rB) Make a backup of the entire inventory
            \rQ) Quit the app''')
        choice = input('\nWhat would you like to do? ').lower().strip()
        if choice in ['v','n','a','b','q']:
            return choice
        else: 
            input('''\n****** EEROR ******
                  \nPlease choose only the options above.
                  \rPress ENTER to try again.''')


def clean_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%Y').date()
    except ValueError:
        print(f'''
            \n****** DATE ERROR ******
            \nInvalid date format 
            \n{date_str} needs to be a valid date and in mm/dd/yyyy format
            \n************************''')
        return None


def clean_price(price_str):
    try:
        price_str = price_str.replace('$', '')
        return int(float(price_str) * 100)       
    except ValueError:
        print(f'''
                \n****** PRICE ERROR ******
                \nInvalid price format 
                \n{price_str} needs to be in a valid price format 
                \nEx: 10.99
                \n*************************''')
        return None


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        print(f'''
                \n****** ID ERROR ******
                \nInvalid ID 
                \n{id_str} needs to be a number
                \nPress ENTER to try again..
                \n*************************''')
        return None
    else:
        if product_id in options:
            return product_id
        else:
            print(f'''
                \n****** ID ERROR ******
                \nInvalid ID 
                \n"{id_str}" needs to be a number within the Product ID range above
                \nPress ENTER to try again..
                \n*************************''')
            return


def initialize_brands_csv():
    brands_added = []
    with open('brands.csv') as brands_CSV:
        data = csv.reader(brands_CSV)
        next(data)
        for row in data:
            brand_name = row[0]
            if brand_name not in brands_added:
                brand_in_db = session.query(Brands).filter(Brands.brand_name == row[0]).one_or_none()
                if brand_in_db is None:
                    new_brand = Brands(brand_name=brand_name)
                    session.add(new_brand)
                    brands_added.append(new_brand)
                else:
                    brands_added.append(brand_in_db)

                    # DEBUG
                    print(f'Brand {row[0]} already exists in the database.')
        session.commit()
        print(f"Added {len(brands_added)} brands from brands.csv")
        return brands_added            


def initialize_inventory_csv(existing_brands):
    try:
        with open('inventory.csv') as inventory_CSV:
            data = csv.reader(inventory_CSV)
            next(data)
            for row in data:            
                product_name = row[0].strip()  
                product_price = clean_price(row[1].strip())  
                product_quantity = int(row[2].strip())   
                date_updated = clean_date(row[3].strip())  
                brand_name = row[4].strip()  
                # Ensure that the price and date are valid
                if product_price is not None and date_updated is not None:
                    # Check if the brand already exists in the database
                    brand = check_for_existing_brands(brand_name)
                    if brand:
                        brand_id = brand.brand_id
                    else:
                        # Create a new brand
                        brand = Brands(brand_name=brand_name)
                        session.add(brand)
                        session.flush()
                        brand_id = brand.brand_id

                    # Check if the product already exists in the database
                    existing_product = session.query(Products).filter(
                        Products.product_name == product_name,
                        Products.brand_id == brand_id
                    ).first()

                    if existing_product:
                        # Update the existing product
                        existing_product.product_quantity = product_quantity
                        existing_product.date_updated = date_updated
                        session.add(existing_product)
                    else:
                        # Add a new product
                        new_product = Products(
                            product_name=product_name,
                            product_price=product_price,
                            product_quantity=product_quantity,
                            date_updated=date_updated,
                            brand_id=brand_id
                        )
                        session.add(new_product)
            session.commit()
            print("Inventory data added successfully.")
    except FileNotFoundError:
        print("inventory.csv file not found.")
    except Exception as e:
        print(f"Error processing inventory.csv: {e}")


def check_for_existing_brands(brand_name):
    try:
        return session.query(Brands).filter(Brands.brand_name == brand_name).one_or_none()
    except sqlalchemy.exc.MultipleResultsFound:
        print(f"You are duplicating an item with the brand name of '{brand_name}'. We'll use the one thats already in the Database")
        return session.query(Brands).filter(Brands.brand_name == brand_name).first()


def check_for_existing_product(name, brand_id):
    return session.query(Products).filter(
        Products.product_name == name,
        Products.brand_id == brand_id
    ).one_or_none()


def get_product_id_range():
    min_id = session.query(func.min(Products.product_id)).scalar()
    max_id = session.query(func.max(Products.product_id)).scalar()
    return min_id, max_id


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            min_id, max_id = get_product_id_range()
            id_options = []
            for product in session.query(Products):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nProduct ID Range: {min_id}-{max_id}
                    \nWhich Product ID do you want to view: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Products).filter(Products.product_id == id_choice).first()
            print(f'''
                  \nID: {the_product.product_id}
                  \rName: {the_product.product_name}
                  \rQuantity: {the_product.product_quantity}
                  \rPrice: {the_product.product_price}
                  \rLast Updated: {the_product.date_updated.strftime('%m/%d/%Y')}
                  ''')
        elif choice == 'n':
            # Add product
                name = input('What is the name of the product: ')
                price_error = True
                while price_error:
                    price = input('How much does it cost (Ex: 10.99): ')
                    price = clean_price(price)
                    if type(price) == int:
                        price_error = False
                        print(price)
                quantity = input('How many are in stock: ')
                # Date Updated...How do I add the current timestamp for record being committed/updated
                date_error = True
                while date_error:
                    date = input('Created date (Ex: 10/01/2019): ')
                    date = clean_date(date)
                    if date is not None:
                        date_error = False
                brand = input('What is the brand name: ') 

                # checking for duplicates
                brand_in_db = session.query(Brands).filter(Brands.brand_name == brand).one_or_none()
                brand_id = brand_in_db.brand_id if brand_in_db else None
                products_in_db = check_for_existing_product(name, brand_id)
                if products_in_db:
                    user_choice = input(f'"{name}" is already in the Inventory. Shall we update the record? (y/n): ').strip().lower()
                    if user_choice == 'y':
                        products_in_db.product_name = name
                        products_in_db.product_quantity = quantity
                        products_in_db.date_updated = date
                        session.add()
                        session.commit()
                        print(f'You have successfully updated {name}')
                    else:
                        print('Product addition canceled...')
                else:
                    new_product = Products(product_name = name,product_price = price, product_quantity = quantity, date_updated = date)
                    new_brand = Brands(brand_name = brand)

                    session.add(new_product)
                    session.add(new_brand)
                    session.commit()
                    print(f'''\nSummary of product added to inventory:
                            \nProduct Name: {name}
                            \rProduct Cost: {price}
                            \rProduct QTY: {quantity}
                            \rProduct Brand: {brand}
                        ''')
        elif choice == 'a':
            # Analyze the inventory by:
                # most expensive brand
                # most common brand
                # Brand with the largest inventory
                # least expensive product
                # total inventory value
                
                # Press ENTER to return to the main menu..
            pass
        elif choice == 'b':
            # Create a backup of the inventory to a csv file
                # Needs to create a csv file with the following constraints:
                    # header row with the field titles
                    # Each product is its own row, with each field vaule seperated by a comma
                    # must be saved in the same directory as the app.py file
                    # date is in the same format as the original csv file (m/d/yyyy)
                    # price is in the same format as the original csv file ($0.00) rather than cents
                # Prompt the user to name the backup file
                # Display the message that the backup was successful
                # If the backup was not successful, display the error message
                # Press ENTER to return to the main menu..
            pass
        elif choice == 'q':
            print('\n****** EXITING THE APP! ******')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    existing_brands = initialize_brands_csv()
    initialize_inventory_csv(existing_brands)
    app()