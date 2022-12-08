from SQL_Connection import start_connection
import mysql.connector
from verification import check

connection = start_connection()

adminstrator = check(connection)

if adminstrator == True:
    import admin
else:
    import customer
