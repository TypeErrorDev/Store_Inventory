# import csv
#
# This will read the csv file and print the brand names
# with open('csv/inventory.csv', newline='') as csvfile:
#     artreader = csv.DictReader(csvfile, delimiter=',')
#     rows = list(artreader)
#     for row in rows[1:]:
#         print(row['brand_name'])
#
#
# import csv
#
# with open('csv/inventory.csv', 'a') as csvfile:
#     fieldnames = ['product_id', 'product_name', 'product_quantity', 'product_price', 'date_updated', 'brand_id']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow({'product_id': 1, 'product_name': 'Pencil', 'product_quantity': 10, 'product_price': 2, 'date_updated': '2020-01-01', 'brand_id': 1})
#     writer.writerow({'product_id': 2, 'product_name': 'Pen', 'product_quantity': 5, 'product_price': 3, 'date_updated': '2020-01-01', 'brand_id': 1})
#
#     # This will read the csv file and print the brand names