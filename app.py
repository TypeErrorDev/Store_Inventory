from models import (Base, session, Products, Brands, engine)


def menu():
    while True:
        print('''
            \n****** MAIN MENU ******
              \rV) View a single product's inventory 
              \rN) Add a new product to the database
              \rA) View an analysis of the inventory
              \rB) Make a backup of the entire inventory''')
        input('What would you like to do? ').lower().strip()


# main menu - add, search, analysis, exit, view
# add - add a new record
# edit books
# delete books
# search - search for a book
# data cleaning - remove duplicates
# loop runs program



if __name__ == '__main__':
    Base.metadata.create_all(engine)
    menu()