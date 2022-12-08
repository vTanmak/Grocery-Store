from SQL_Connection import start_connection
from tabulate import tabulate
from random import randint
from datetime import datetime

connection = start_connection()
cursor = connection.cursor()

def Check_Cart():
    L = [["Product ID","Product Name","Quantity","Price Per Unit","Total Price"]]
    sql = "SELECT * FROM order_details"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2],i[3],i[4]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    print()
    return data

def Add_Product():
    L = [["Product ID","Product Name","Price Per Unit"]]
    sql = "SELECT * from products"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    search = (int(input("Enter the product id to add the product: ")))
    found = False
    for i in data:
        if i[0] == search:
            found = True
            product_id = i[0]
            product_name = i[1]
            product_price = i[2]
    if found:
        total_price = product_price*1
        insert_sql = "INSERT INTO order_details values({},'{}',{},{},{})".format(product_id,product_name,1,product_price,total_price)
        cursor.execute(insert_sql)
        connection.commit()
        print("Product successfully added in cart.")
    else:
        print("Product not found.")

def Delete_Product():
    L = [["Product ID","Product Name","Quantity","Price"]]
    sql = "SELECT * FROM order_details"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2],i[3]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    product_id = (int(input("Enter the product id to remove from the cart: ")))
    found = False
    for i in data:
        if i[0] == product_id:
            found = True
            break
    if found:
        delete_sql = "DELETE FROM order_details WHERE product_id = '{}'".format(product_id,)
        cursor.execute(delete_sql)
        connection.commit()
        print("Product successfully delete from the cart.")
    else:
        print("Product not found in the cart.")

def Update_Product():
    data = Check_Cart()
    search = (int(input("Enter the produt id to update the product: ")))
    found = False
    for i in data:
        if i[0] == search:
            found = True
            price = i[3]
            break
    if found:
        quantity = (int(input("Enter the new quantity: ")))
        new_price = price*quantity
        update_sql = "UPDATE order_details SET quantity= {} WHERE product_id = {}".format(quantity,search)
        cursor.execute(update_sql)
        update_sql = "UPDATE order_details SET total_price= {} WHERE product_id = {}".format(new_price,search)
        cursor.execute(update_sql)
        print("Product successfully updated.")
    else:
        print("Product not found.")

def Generate_Bill():
    gen = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
    'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y',
    'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    name = (input("Enter your name: "))
    phone_number = (int(input("Enter your phone number: ")))
    current = datetime.now()
    date_time = current.strftime("%Y/%m/%d %H:%M:%S")
    order_id = ""
    for i in range(15):
        order_id += gen[randint(0,len(gen)-1)]
    L = [["Product ID","Product Name","Quantity","Price Per Unit","Total Price"]]
    sql = "SELECT * FROM order_details"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2],i[3],i[4]]
        L.append(temp_list)
    total = 0 
    for i in data:
        total += i[4]
    gst = 0.18*total
    CSGT = SGST = gst/2
    print()
    print("Name of the customer: ",name)
    print("Phone Number of the customer: ",phone_number)
    print("Order ID: ",order_id)
    temp_list=["","Total","","",total]
    temp_list1=["","GST","","",gst]
    temp_list2=["","Final Total","","",total+gst]
    L.append(temp_list)
    L.append(temp_list1)
    L.append(temp_list2)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    print("CSGT: ",CSGT)
    print("SGST: ",SGST)
    cursor.execute("INSERT INTO orders VALUES('{}','{}',{},'{}')".format(order_id,name,total,date_time))
    connection.commit()
    cursor.execute("DELETE FROM order_details")
    connection.commit()


while True:
    print("------------------Welcome Customer------------------")
    print()
    print("1. Check your cart.")
    print("2. Add a new product in your cart")
    print("3. Remove a product from your cart")
    print("4. Update the quantity of a product in your cart.")
    print("5. Generate bill.")
    print("6. Exit")
    print()

    try:
        choice = (int(input("Enter your choice: ")))
    except ValueError:
        print("The number should be a integer.")

    if choice == 1:
        Check_Cart()

    if choice == 2:
        Add_Product()

    if choice == 3:
        Delete_Product()

    if choice == 4:
        Update_Product()

    if choice == 5:
        Generate_Bill()

    if choice == 6:
        print("Exiting program.")
        print("Thank you. Hope you have a great day!")
        print("----------------------------------------------------------")
        break

connection.close()
