#Run this file before running the main program for the proper functioning of the program

import mysql.connector as sql
db = sql.connect(host='localhost',user='root',password='****')
cursor = db.cursor()


cursor.execute("CREATE DATABASE IF NOT EXISTS grocery_shop")
db.commit()
print("Database successfully created.")


cursor.execute("USE grocery_shop")


cursor.execute("""CREATE TABLE if not exists owner (userid varchar(25) UNIQUE,password varchar(15))""")
try:
        cursor.execute("""INSERT INTO owner VALUES ('admin', 'admin123')""")
        db.commit()
        print("Successfully created owner table and the default admin has been added")
except:
        db.rollback()
        print("The default admin has been already added.")


cursor.execute("""CREATE TABLE if not exists products (product_id INT NOT NULL,name VARCHAR(45) NOT NULL,
price_per_unit DOUBLE NOT NULL,PRIMARY KEY (product_id))""")
db.commit()
print("Successfully created products table.")

#Pre-added products.
sql = "INSERT INTO products VALUES(%s,%s,%s)"
products = [(1,"Sugar (1kg)",50),(2,"Cheese Slice",130),(3,"Butter (200 g)",110),(4,"Onion (1kg)",40),(5,"Potato (1kg)",30),
(6,"Bread",25),(7,"Maggi",12),(8,"Salt (1 kg)",50),(9,"Tomato (1 kg)",16),(10,"Soft Drink (500 ml)",40),(11,"Soft Drink (1 L)",60),
(12,"Biscuits",35),(13,"Chocolate Biscuits",50),(14,"Chips",20),(15,"Coffee",70),(16,"Tea Leaves",60),(17,"Rice (1kg)",140),
(18,"Grapes (1kg)",150),(19,"Oranges",60),(20,"Apples",180),(21,"Carrot",60),(22,"Mushroom (200 g)",60),(23,"Broccoli (300 g)",25),
(24,"Curd (400 g)",65),(25,"Toothpaste",90),(26,"Wheat Flour",25),(27,"Mixed Fruit Juice (1 L)",100),(28,"Chocolate",75),
(29,"Ice Cream", 40),(30,"Tomato Sauce (1 kg)",120)]

try:
        cursor.executemany(sql,products)
        db.commit()
        print("Successfully added products in product table")
except:
        print("Products were already added in the table.")
        db.rollback()

cursor.execute("""
CREATE TABLE if not exists order_details
(Product_ID INT NOT NULL PRIMARY KEY,
Product_Name varchar(50) NOT NULL,
Quantity INT NOT NULL,
Price_Per_Unit INT NOT NULL,
Total_Price FLOAT NOT NULL)""") 
db.commit()
print("Successfully created order details table")


cursor.execute("""
CREATE TABLE if not exists orders 
(order_id varchar(20) NOT NULL,
customer_id INT NOT NULL,
customer_name VARCHAR(100) NOT NULL,
total DOUBLE NOT NULL,
datetime DATETIME NOT NULL,
PRIMARY KEY (order_id));
""")
db.commit()
print("Successfully created orders table")


cursor.execute("""
CREATE TABLE if not exists user_information
(customer_id int NOT NULL UNIQUE,
name varchar(40) NOT NULL,
email_id VARCHAR(100) NOT NULL,
phone_number BIGINT NOT NULL,
password varchar(30) NOT NULL,
PRIMARY KEY (email_id));
""")
db.commit()
print("Successfully created user information table.")

db.close()
