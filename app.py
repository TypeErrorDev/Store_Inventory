from models import Base, session, Products, Brands, engine
import datetime
import csv

# to run the app, go to .\env\Scripts\activate and the python app.py



def menu():
    # create menu for ONLY allowing the following options
    # 'v' (View a single product's inventory),
    # 'n' (Add a new product to the database),
    # 'a' (View an analysis),
    # 'b' (Make a backup of the entire inventory),
    # 'x' (Exit app)
    while True:
        print('''
            \n****** Inventory Menu ******
            \nV) View a single product's inventory
            \rN) Add a new product to the database
            \rA) View the analysis options
            \rB) Make a backup of the entire inventory
            \rX) Exit the app''')
        choice = input('\nWhat would you like to do? ').lower().strip()
        if choice in ['v','n','a','b','x']:
            return choice
        else: 
            input('''\n****** EEROR ******
                  \nPlease choose only the options above.
                  \rPress ENTER to try again.''')
    


def clean_date(date_str):
    pass


def clean_price(price_str):
    pass


def add_brands_csv():
    pass


def add_inventory_csv():
    pass


def check_existing_brands():
    pass


def check_exisiting_product():
    pass


def app():
    app_running = True

    while app_running:
        choice = menu()

        if choice == 'v':
            pass
        if choice == 'n':
            pass
        if choice == 'a':
            pass
        if choice == 'n':
            pass
        else:
            print('\n****** GOODBYE MY FRIENDS! ******')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # existing_brands = add_brands_from_csv()
    # add_inventory_from_csv(existing_brands)
    app()
