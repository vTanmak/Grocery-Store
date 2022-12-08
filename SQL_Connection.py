import mysql.connector

connect = None

def start_connection():
  print("Opening SQL connection")
  print()
  global connect

  if connect is None:
    connect = mysql.connector.connect(user='root', password='Pinanatan@112029', database='grocery_shop')
    #Write the correct password for SQL Database connection
    
  return connect
