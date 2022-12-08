from SQL_Connection import start_connection
from tabulate import tabulate

connection = start_connection()
cursor = connection.cursor()

def Add_Product():
    sql = "INSERT INTO PRODUCTS VALUES(%s,%s,%s)"
    product_id = (int(input("Enter Product ID: ")))
    product_name = (input("Enter name of the Product: "))
    product_price = (float(input("Enter price of the Product: ")))
    value = [product_id,product_name,product_price]
    cursor.execute(sql,value)
    connection.commit()
    print("Product has been successfully added.")
    print()

def Delete_Product():
    search = (int(input("Enter the product id: ")))
    found = False
    cursor.execute("SELECT * FROM PRODUCTS")
    data = cursor.fetchall()
    for i in data:
        if i[0] == search:
            found = True
            break
    if found == True:
        sql = "DELETE FROM PRODUCTS WHERE product_id = {}".format(search,)
        cursor.execute(sql)
        connection.commit()
        print("Product has been found and successfully deleted.")
    else:
        print("Product not found.")
    print()
    
def Update_Product():
    search = (int(input("Enter the product id: ")))
    found = False
    cursor.execute("SELECT * FROM PRODUCTS;")
    data = cursor.fetchall()
    for i in data:
        if i[0] == search:
            found = True
            break
    if found == True:
        new_price = (int(input("Enter new price: ")))
        sql = "UPDATE products SET price_per_unit= '{}' WHERE product_id = '{}'".format(new_price,search)
        cursor.execute(sql)
        connection.commit()
        print("Product has been found and successfully update.")
    else:
        print("Product not found.")
    print()

def Check_Last_Orders():
    print("Details of the order by the customer: ")
    print()
    L = [["Order ID","Customer Name","Total Price","Date and Time"]]
    sql = "SELECT * FROM orders"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2],i[3]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    print()

print("------------------Welcome Adminstrator------------------")
print()
while True:
    print("-------------------Adminstrator Options-------------------")
    print()
    print("1. Add a new product.")
    print("2. Delete a existing product.")
    print("3. Update a existing product.")
    print("4. Check the previous order details.")
    print("5. Exit")
    print()
    choice = (int(input("Enter your choice: ")))
    
    if choice == 1:
        Add_Product()

    elif choice == 2:
        Delete_Product()

    elif choice == 3:
        Update_Product()
    
    elif choice == 4:
        Check_Last_Orders()

    elif choice == 5:
        print("Exiting the program.")
        print("----------------------------------------------------------------")
        break

    else:
        print("Invalid Input.")

connection.close()
