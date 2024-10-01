from models import Base, session, Products, Brands, engine
from datetime import datetime
from sqlalchemy import func
import csv
# import time


def menu():
    while True:
        print('''
            \n****** Main Inventory Menu ******
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
                    # print(f'Brand {row[0]} already exists in the database.')
        session.commit()
        # DEBUG
        # print(f"Added {len(brands_added)} brands from brands.csv")
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


def get_ranked_products():
    ranked_products = session.query(Products).order_by(Products.product_id).all()
    return {rank + 1: product.product_id for rank, product in enumerate(ranked_products)}


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v': # View a Product
            ranked_products = get_ranked_products()
            max_rank = len(ranked_products)
            id_options = []
            for product in session.query(Products):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                rank_choice = input(f'''
                    \n****** View a Product ******
                    \nProduct: 1-{max_rank}
                    \nWhich Product ID do you want to view: ''')
                try:
                    rank_choice = int(rank_choice)
                    if 1 <= rank_choice <= max_rank:
                        id_choice = ranked_products[rank_choice]
                        id_error = False
                    else:
                        print(f"Please enter a number between 1 and {max_rank}.")
                except ValueError:
                    print("Please enter a valid number.")
                # handle the case where the user enters a number that is not in the list
            the_product = (
                session.query(Products)
                .join(Brands, Products.brand_id == Brands.brand_id)
                .filter(Products.product_id == id_choice)
                .first()
                )
            if the_product:
                print(f'''
                    \n****** Product Info ******
                    \rBrand: {the_product.brand.brand_name}
                    \rName: {the_product.product_name}
                    \rQuantity: {the_product.product_quantity}
                    \rPrice: ${the_product.product_price / 100:.2f}
                    \rLast Updated: {the_product.date_updated.strftime('%m/%d/%Y')}
                    ''')
                
                choice = input(f'''
                            \n****** Update/Delete Product? ******
                            \nU) Update the product
                            \nD) Delete the product
                            \nPress ENTER to return to the main menu..
                            ''' ).strip().lower()
                match choice:
                    case 'u':
                        session.query(Products).filter(Products.product_id == id_choice).update({
                            Products.product_name: input('What is the new name: '),
                            Products.product_price: clean_price(input('What is the new price: ')),
                            Products.product_quantity: input('What is the new quantity: '),
                            Products.date_updated: clean_date(input('What is the new date: '))
                        })
                        session.commit()
                        print('Product updated successfully!')
                    case 'd':
                        session.query(Products).filter(Products.product_id == id_choice).delete()
                        session.commit()
                        print('Product deleted successfully!')
                    case _:
                        continue
            else:
                print(f'No product found with the ID of {id_choice}')
        elif choice == 'n': # Add product
            print(f'''
                  \n****** Add A Product ******
                    ''')
            name = input('What is the name of the product: ')
            price_error = True
            while price_error:
                price = input('How much does it cost (Ex: 10.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity = input('How many are in stock: ')
            date_error = True
            while date_error:
                date = input('Created date (Ex: 10/01/2019): ')
                date = clean_date(date)
                if date is not None:
                    date_error = False
            brand = input('What is the brand name: ').strip()

            # Check if the brand exists, if not create it
            brand_in_db = session.query(Brands).filter(Brands.brand_name == brand).one_or_none()
            if not brand_in_db:
                new_brand = Brands(brand_name=brand)
                session.add(new_brand)
                session.flush()  # This will assign an ID to the new brand
                brand_id = new_brand.brand_id
            else:
                brand_id = brand_in_db.brand_id

            # Check for existing product
            existing_product = check_for_existing_product(name, brand_id)
            
            if existing_product:
                print(f'"{name}" already exists. Updating the record.')
                existing_product.product_quantity = quantity
                existing_product.product_price = price
                existing_product.date_updated = date
                session.add(existing_product)
            else:
                new_product = Products(
                    product_name=name,
                    product_price=price, 
                    product_quantity=quantity, 
                    date_updated=date,
                    brand_id=brand_id
                )
                session.add(new_product)
            session.commit()
            print(f'Product "{name}" has been added/updated successfully with brand_id: {brand_id}')
        elif choice == 'a': # Analyze the inventory by:
            print(f'''
                \n****** Product Analysis ******
                \nA) Most expensive product?
                \rB) Least expensive product? 
                \rC) Most common brand in inventory?
                \rD) Product with the most on hand quantity?
                \rE) Total inventory value?
                ''')
            analysis_choice = input('\nWhat would you like to do? ').lower().strip()

            if analysis_choice == "a": # most expensive brand #DONE
                most_expensive_product = (
                    session.query(Products, Brands)
                    .join(Brands)
                    .order_by(Products.product_price.desc())
                    .first()
                )
                if most_expensive_product:
                    product, brand = most_expensive_product
                    print(f'''
                            \n***** Most Expensive Product *****
                            \nName: {product.product_name}
                            \rBrand: {brand.brand_name}
                            \rPrice: ${product.product_price / 100:.2f}
                            \rQuantity: {product.product_quantity}
                            ''') 
                else:
                    print("No products found...")
            elif analysis_choice == "b": # least expensive product #DONE
                least_expensive_product = (
                    session.query(Products, Brands)
                    .join(Brands)
                    .order_by(Products.product_price)
                    .first()
                )
                if least_expensive_product:
                    product, brand = least_expensive_product
                    print(f'''
                            \n***** Least Expensive Product *****
                            \nName: {product.product_name}
                            \rBrand: {brand.brand_name}
                            \rPrice: ${product.product_price / 100:.2f}
                            \rQuantity: {product.product_quantity}
                            ''') 
                else:
                    print("No products found...")
            elif analysis_choice == "c":  # most common brand #DONE
                most_common_brand = (
                    session.query(Brands.brand_name, func.count(Products.product_id)
                                .label('most_common_brand'))
                                .join(Products, Brands.brand_id == Products.brand_id)
                                .group_by(Brands.brand_name)
                                .order_by(func.count(Products.product_id)
                                .desc())
                                .first()
                            )
                if most_common_brand:
                    brand_name, product_count = most_common_brand
                    print(f'''
                        \n***** Most Common Brand *****
                        \nBrand Name: {brand_name}
                        \rProduct Count: {product_count}
                    ''')
                else:
                    print("No brands found in the database.")
            elif analysis_choice == "d":  # Brand with the largest inventory #DONE
                product_with_most_quantity = (
                    session.query(
                        Products.product_name,
                        Brands.brand_name,
                        Products.product_quantity
                    )
                    .join(Brands, Products.brand_id == Brands.brand_id)
                    .order_by(Products.product_quantity.desc())
                    .first()
                )
                if product_with_most_quantity:
                    product_name, brand_name, quantity = product_with_most_quantity
                    print(f'''
                        \n***** Product with Most Quantity *****
                        \nName: {product_name}
                        \rBrand: {brand_name}
                        \rQuantity: {quantity}
                    ''')
                else:
                    print("No products found...")
            elif analysis_choice == "e": # total inventory value
                
                pass
            else: # Press ENTER to return to the main menu..
                pass
        elif choice == 'b': # Create a backup of the inventory to a csv file
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
        elif choice == 'q': # Quit the app
            print('\n****** EXITING THE APP! ******')
            app_running = False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    existing_brands = initialize_brands_csv()
    initialize_inventory_csv(existing_brands)
    app()