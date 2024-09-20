from models import Base, session, Products, Brands, engine
from datetime import datetime
from sqlalchemy import select
import csv

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
        date = datetime.strptime(date_str, '%m/%d/%Y').date()
        return date.strftime('%m/%d/%Y')
    except ValueError:
        print(f'''
              \n****** DATE ERROR ******
              \nInvalid date format 
              \n{date_str} needs to be a valid date and in mm/dd/yyyy format
              \n************************''')
        return


def clean_price(price_str):
    try:
        price_str = price_str.replace('$', '')
        price = float(price_str)
        price = round(price, 2)
        print( int(price) if price.is_integer() else price)
    except ValueError:
        print(f'''
                \n****** PRICE ERROR ******
                \nInvalid price format 
                \n{price_str} needs to be in a valid price format 
                \nEx: 10.99
                \n*************************''')
        return None


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
    products_added = 0
    with open('inventory.csv') as inventory_CSV:
        data = csv.reader(inventory_CSV)
        next(data)
        for row in data:
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = int(row[2])
            date_updated = clean_date(row[3])
            brand = row[4]
            


def check_existing_brands():
    pass


def check_exisiting_product():
    pass


def app():
    app_running = True

    while app_running:
        choice = menu()

        if choice == 'v':
            # View a single product's inventory by product_id
                # dynamically display the product_id's (first product_id - last product_id)
                # *** product_name ***
                # Price: 
                # Quantity:
                # Brand:
                # Last Updated: (dynamic date)

                # Update the product: send to 'n' option
                # Delete the product: run the delete function
                # ************************

                # Press ENTER to return to the main menu..
            pass
        if choice == 'n':
            # What is the name of the product?
            # How much does it cost?
            # How many are in stock?
            # What is the brand name?
                # If there is a duplicate product_name and brand, prompt the user to see if they want to update the prouct 
                    # if not, then cancel and return to the main menu
                    # if they do want to update the product, then the product will be updated with the new information and the user will be notified "{product_name} has been Updated"
                    # if there is a new brand, ensure to update the brand table with the new brand
            # Return a summary of the product that was added
            pass
        if choice == 'a':
            # Analyze the inventory by:
                # most expensive brand
                # most common brand
                # Brand with the largest inventory
                # least expensive product
                # total inventory value
                
                # Press ENTER to return to the main menu..
            pass
        if choice == 'b':
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
        else:
            print('\n****** EXITING THE APP! ******')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    existing_brands = initialize_brands_csv()
    initialize_inventory_csv(existing_brands)
    app()

    # clean_price("15.55")