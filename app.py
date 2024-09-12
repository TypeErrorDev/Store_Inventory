from models import (Base, session, Products, Brands, engine)
import datetime
import csv


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

def clean_price(price_str):
    price_float = float(price_str)
    print(price_float)


    

def add_csv():
        with open('./csv/inventory.csv') as csvfile:
            data = csv.reader(csvfile)
            for row in data:
                product_name = row[0]
                product_price = row[1]
                product_quantity = row[2]
                date_updated = row[3]
                brand_name = row[4]
                print(row)



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
        else:
            print('GOODBYE FRIENDS!')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    # app()
    # add_csv()
    clean_price('9.34')