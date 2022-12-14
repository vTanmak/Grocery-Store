from SQL_Connection import start_connection
from tabulate import tabulate
from random import randint
from datetime import datetime
import mysql.connector

connection = start_connection()
cursor = connection.cursor()

def create_order_details_table(name_of_table):
    try:
        cursor.execute("""
        CREATE TABLE if not exists {}
        (Product_ID INT NOT NULL PRIMARY KEY,
        Product_Name varchar(50) NOT NULL,
        Quantity INT NOT NULL,
        Price_Per_Unit INT NOT NULL,
        Total_Price FLOAT NOT NULL)""".format(name_of_table)) 
        connection.commit()
    except:
        print("An error has occured while creating order details table or table already exist.")
        connection.rollback()


def customer_login():
    logged_in = False
    while logged_in == False:
        choice = (input("Do you want to login or sign in (login/sign) ? "))
        choice = choice.lower()
        if choice == "login":
            while True:
                email = (input("Enter email id: "))
                email = email.lower()
                password = (input("Enter password: "))
                cursor.execute("SELECT * FROM user_information")
                data = cursor.fetchall()
                for i in data:
                    if i[2] == email and i[4] == password:
                        logged_in = True
                        customer_id = i[0]
                        name = i[1]
                        phone_number = i[3]
                if logged_in:
                    print("You are logged in as:",name)
                    break
                else:
                    print("Email ID/Password is incorrect or does not exist.")
          
        elif choice == "sign":
            name = (input("Enter your name: "))
            email = (input("Enter email id: "))
            email = email.lower()
            email_copy = email.strip()
            email_copy = email.split("@")
            if len(email_copy) != 2:
                print("The email is invalid.")
                continue
            cursor.execute("SELECT email_id FROM user_information")
            data = cursor.fetchall()
            email_exist = False
            for i in data:
                if email == i[0]:
                    email_exist = True
            if email_exist:
                print("The Email ID is already used.")
                continue
            password = (input("Enter password: "))
            phone_number = (int(input("Enter phone number: ")))
            cursor.execute("SELECT * FROM user_information")
            data = cursor.fetchall()
            customer_id = len(data) + 1
            cursor.execute("INSERT INTO user_information VALUES({},'{}','{}',{},'{}')".format(customer_id,name,email,phone_number,password))
            connection.commit()
            logged_in = True
            print("You are logged in as: ",name)
            print()
            
        else:
            print("Invalid Choice.")
            
    return (name,customer_id,phone_number)

def Check_Cart():
    print()
    print("Your cart: ")
    L = [["Product ID","Product Name","Quantity","Price Per Unit","Total Price"]]
    sql = "SELECT * FROM {}".format(table_name)
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
        try:
            total_price = product_price*1
            insert_sql = "INSERT INTO {} values({},'{}',{},{},{})".format(table_name,product_id,product_name,1,product_price,total_price)
            cursor.execute(insert_sql)
            connection.commit()
            print("Product successfully added in cart.")
        except mysql.connector.IntegrityError:
            print("The product is already in the cart. To update the product please select the update product option.")
    else:
        print("Product not found.")
    print()

def Delete_Product():
    L = [["Product ID","Product Name","Quantity","Price"]]
    sql = "SELECT * FROM {}".format(table_name,)
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
        delete_sql = "DELETE FROM {} WHERE product_id = {}".format(table_name,product_id)
        cursor.execute(delete_sql)
        connection.commit()
        print("Product successfully deleted from the cart.")
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
        update_sql = "UPDATE {} SET quantity= {} WHERE product_id = {}".format(table_name,quantity,search)
        cursor.execute(update_sql)
        update_sql = "UPDATE {} SET total_price= {} WHERE product_id = {}".format(table_name,new_price,search)
        cursor.execute(update_sql)
        print("Product successfully updated.")
    else:
        print("Product not found.")

def Generate_Bill():
    gen = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q','R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
    'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'm', 'n', 'o', 'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y',
    'z','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    current = datetime.now()
    date_time = current.strftime("%Y/%m/%d %H:%M:%S")
    order_id = ""
    while True:
        for i in range(15):
            order_id += gen[randint(0,len(gen)-1)]
        cursor.execute("SELECT order_id from orders")
        data = cursor.fetchall()
        exist = False
        for j in data:
            if j[0] == order_id:
                exist = True
        if exist:
            continue
        else:
            break
    L = [["Product ID","Product Name","Quantity","Price Per Unit","Total Price"]]
    sql = "SELECT * FROM {}".format(table_name,)
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
    final_total = total + gst
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
    cursor.execute("INSERT INTO orders VALUES('{}',{},'{}',{},'{}')".format(order_id,customer_id,name,final_total,date_time))
    connection.commit()
    cursor.execute("DELETE FROM {}".format(table_name,))
    connection.commit()
    print()
    print("Thank you for purchasing.")
    print()

data = customer_login()
customer_id = data[1]
name = data[0]
phone_number = data[2]

table_name = str(customer_id) + "_order_details"
create_order_details_table(table_name)
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

    choice = (input("Enter your choice: "))
    choice = choice.strip()
    if choice == "1":
        Check_Cart()

    if choice == "2":
        Add_Product()

    if choice == "3":
        Delete_Product()

    if choice == "4":
        Update_Product()

    if choice == "5":
        Generate_Bill()

    if choice == "6":
        print("Exiting program.")
        print("Thank you. Hope you have a great day!")
        print("----------------------------------------------------------")
        break

connection.close()
