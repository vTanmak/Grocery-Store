from SQL_Connection import start_connection
from tabulate import tabulate
from datetime import datetime

connection = start_connection()
cursor = connection.cursor()

def Add_Product():
    sql = "INSERT INTO PRODUCTS VALUES(%s,%s,%s)"

    product_id = (int(input("Enter Product ID: ")))
    cursor.execute("SELECT product_id from products")
    data = cursor.fetchall()
    exist = False
    for i in data:
        if i[0] == product_id:
            exist = True
    if exist:
        print("A product already exist with that product ID")
        print()
        return
    product_name = (input("Enter name of the Product: "))
    product_price = (float(input("Enter price of the Product: ")))
    value = [product_id,product_name,product_price]
    cursor.execute(sql,value)
    connection.commit()
    print("Product has been successfully added.")
    print()

def Delete_Product():
    L = [["Product ID","Product Name","Price Per Unit"]]
    sql = "SELECT * from products"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    search = (int(input("Enter the product id of the product to delete: ")))
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
    L = [["Product ID","Product Name","Price Per Unit"]]
    sql = "SELECT * from products"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
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
        print("Product has been found and successfully updated.")
    else:
        print("Product not found.")
    print()

def Check_Orders():
    print("Details of the order by the customer: ")
    print()
    L = [["Order ID","Customer ID","Customer Name","Total Price","Date and Time"]]
    sql = "SELECT * FROM orders"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in data:
        temp_list = [i[0],i[1],i[2],i[3],i[4]]
        L.append(temp_list)
    print(tabulate((L),headers="firstrow",tablefmt="psql"))
    print()

def Search_Order_Details():
    print()
    print("I. Search by Order ID")
    print("II. Search by Price")
    print("III. Search by Name of the Customer")
    print("IV. Search by Date")
    print("V. Search by Customer ID")
    ch = (input("Enter your choice: "))
    ch = ch.upper()

    if ch == "I":
        order_id = (input("Enter order id: "))
        sql = "SELECT * FROM ORDERS WHERE ORDER_ID = '{}'".format(order_id,)
        cursor.execute(sql)
        data = cursor.fetchone()
        if len(data) == 0:
            print("Product not found.")
        else:
            customer_id = data[1]
            name = data[2]
            total = data[3]
            datetime = data[4]
            print()
            print("Customer ID:",customer_id)
            print("Name: ",name)
            print("Total: ",total)
            print("Date and Time when purchased products: ",datetime)

    elif ch == "II":
        print()
        print("a) Display all the orders which has higher price than the given price.")
        print("b) Display all the orders which has lower price than the given price.")
        print("c) Search orders in range of price")
        choi = (input("Enter your choice (a/b/c): "))
        choi = choi.lower()
        print()
        if choi == "a":
            range = (int(input("Enter the price to display the orders higher than that price: ")))
            sql = "SELECT * FROM ORDERS WHERE total > {}".format(range,)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
            print()
            
        elif choi == "b":
            range = (int(input("Enter the price to display the orders lower than that price: ")))
            sql = "SELECT * FROM ORDERS WHERE total < {}".format(range,)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
        elif choi == "c":
            print()
            upper_range = (int(input("Enter upper range of the price: ")))
            lower_range = (int(input("Enter lower range of the price: ")))
            sql = "SELECT * FROM ORDERS WHERE total BETWEEN {} AND {}".format(upper_range,lower_range)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
        else:
            print("Invalid Input.")
        print()
        
    elif ch == "III":
        print()
        name = (input("Enter the name of the customer to search: "))
        sql = "SELECT * FROM orders WHERE customer_name LIKE '%{}%'".format(name)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 0:
            print("No order found.")
        else:
            print()
            L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
            for i in data:
                temp_list = [i[0],i[1],i[2],i[3],i[4]]
                L.append(temp_list)
            print(tabulate((L),headers="firstrow",tablefmt="psql"))

    elif ch == "IV":
        print()
        print("a) Display all the orders which has been placed after the given date")
        print("b) Display all the orders which has been placed before the given date")
        print("c) Display all the orders which has been placed on the given date")
        print("d) Search orders in range of date")
        choi = (input("Enter your choice (a/b/c): "))
        choi = choi.lower()
        print()
        if choi == "a":
            date_range = (input("Enter the date to display the orders placed after that date (Format should be: YYYY-MM-DD): "))
            sql = "SELECT * FROM ORDERS WHERE datetime > '{}'".format(date_range,)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:  
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
        elif choi == "b":
            date_range = (input("Enter the date to display the orders placed before that date (Format should be: YYYY-MM-DD): "))
            sql = "SELECT * FROM ORDERS WHERE datetime < '{}'".format(date_range,)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
        elif choi == "c":
            date_range = (input("Enter the date to display the orders placed on that date (Format should be: YYYY-MM-DD): "))
            sql = "SELECT * FROM ORDERS WHERE DATE(datetime) = '{}'".format(date_range,)
            cursor.execute(sql)
            data = cursor.fetchall()
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
        elif choi == "d":
            upper_range = (input("Enter the date to display the orders placed after that date (Format should be: YYYY-MM-DD): "))
            lower_range = (input("Enter the date to display the orders placed before that date (Format should be: YYYY-MM-DD): "))
            sql = "SELECT * FROM ORDERS WHERE datetime BETWEEN '{}' AND '{}'".format(upper_range,lower_range)
            cursor.execute(sql)
            data = cursor.fetchall()
            print(sql,data)
            if len(data) == 0:
                print("No record found to display.")
            else:
                L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
                for i in data:
                    temp_list = [i[0],i[1],i[2],i[3],i[4]]
                    L.append(temp_list)
                print(tabulate((L),headers="firstrow",tablefmt="psql"))
        else:
            print("Invalid input.")
    
    elif ch == "V":
        c_id = (int(input("Enter the cusomter id to search: ")))
        sql = "SELECT * FROM ORDERS WHERE customer_id = {}".format(c_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 0:
            print("No record found to display.")
        else:
            L = [["Order ID","Cusomter ID","Customer Name","Price","Date Time"]]
            for i in data:  
                temp_list = [i[0],i[1],i[2],i[3],i[4]]
                L.append(temp_list)
            print(tabulate((L),headers="firstrow",tablefmt="psql"))

    else:
        print("Invalid Input.")
    print()
    


print("------------------Welcome Adminstrator------------------")
print()
while True:
    print("-------------------Adminstrator Options-------------------")
    print()
    print("1. Add a new product.")
    print("2. Delete a existing product.")
    print("3. Update a existing product.")
    print("4. Display all the order details.")
    print("5. Search for a order.")
    print("6. Exit")
    print()
    
    choice = (input("Enter your choice: "))
        
    if choice == "1":
        Add_Product()

    elif choice == "2":
        Delete_Product()

    elif choice == "3":
        Update_Product()
    
    elif choice == "4":
        Check_Orders()
    
    elif choice == "5":
        Search_Order_Details()

    elif choice == "6":
        print("Exiting the program.")
        print("----------------------------------------------------------------")
        break

    else:
        print("Invalid Input.")

connection.close()
