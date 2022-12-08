from SQL_Connection import start_connection

connection = start_connection()

def check(connection):
    permission = False
    cursor = connection.cursor()

    adm = (input("Are you a admin (yes/no)? "))
    adm = adm.lower()

    if adm == "yes":
        query = ("SELECT * FROM owner ;")
        cursor.execute(query)
        username = (input("Enter username : "))
        password = (input("Enter password : "))
        data = cursor.fetchall()

        for i in data:
            if username == i[0] and password == i[1]:
                permission = True
                break
    else:
        print("Invalid Information.")
        permission = False
    
    if permission == True:
        print("Admin Verified.")
        print()
    else: 
        print()

    return permission
