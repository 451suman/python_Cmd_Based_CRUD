import sqlite3
import csv
def create_connection():
    try:
        con=sqlite3.connect("user_practise.sqlite3")
        return con
    except Exception as e:
        print(f"Eror = {e}")


#1
def create_table(conn):
    CREATE_USERS_TABLE_QUERY="""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name  CHAR(255) NOT NULL,
            last_name CHAR(255) NOT NULL,
            company_name CHAR(255) NOT NULL,
            address CHAR(255) NOT NULL,
            city CHAR(255) NOT NULL,
            country CHAR(255) NOT NULL,
            state CHAR(255) NOT NULL,
            zip REAL NOT NULL,
            phone1 CHAR(255) NOT NULL,
            phone2 CHAR(255) NOT NULL,
            email CHAR(255) NOT NULL,
            web text
        );
    """
    cur = conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("user table was created successfully")


#2
def read_csv(conn):
    users = []
    with open("sample_users.csv", "r") as f:
        data = csv.reader(f)
        # next(data) 
         # Skip the header row if your CSV has one
        for user in data:
            users.append(tuple(user))
            
        # print(users)
        return users[1:]

#2
def insert_users(conn, users_data):
    #conn = connection function data
    #user_data =  returned data from read_csv () 
    user_add_query = """
        INSERT INTO users(first_name, last_name, company_name, address, city, country, state, zip, phone1, phone2, email, web)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
        """
    cur = conn.cursor()
    cur.executemany(user_add_query, users_data) #(<queryname,<data mith many tupple inside list>)
    conn.commit()
    print(f"{len(users_data)} users were imported successfully.")

#4
def select_user(conn):
    cur = conn.cursor()
    users = cur.execute("SELECT * FROM users ")
    for user in users:
        print (user)

#5
def select_user_by_id(conn, user_id):
    cur = conn.cursor()
    # users = cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    # for user in users:
    #     print(user)
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
        # Check if a user was found
    if user:
        print("User found:", user)
    else:
        print(f"No user found with ID {user_id}")
        return user


INPUT_STRING="""
ENTER THE OPTION:
    1. CREATE TABLE
    2. DUMP USERS FROM CSV INTO USERS TABLE
    3. ADD NEW USER INTO USERS TABLE
    4. QUERY ALL USERS FROM TABLE
    5. QUERY USER BY ID FROM TABLE
    6. QUERY SPECIFIED NO. OF RECORDS FROM TABLE 
    7. DELETE ALL USERS
    8. DELETE USER BY ID
    9. UPDATE USER
    10. PRESS ANY KEY TO EXIT
    """



def main():
    conn = create_connection()
    user_input = input(INPUT_STRING)
    if user_input == "1":
        create_table(conn)
    elif(user_input == "2"):
        users_data =read_csv(conn)
        #return data is stored in user_data 
        # and pass into function insert_users (in parameter)
        insert_users(conn,users_data)
    elif(user_input == "3"):
        pass
    elif(user_input == "4"):
        select_user(conn)
    elif(user_input == "5"):
        user_id = input("Enter user id: ")
        if user_id.isnumeric:
            select_user_by_id(conn,user_id)
    
main()