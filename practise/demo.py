import csv
import sqlite3

def create_connection ():
    try:
        conn = sqlite3.connect("demo.sqlite3")
        return conn
    except Exception as e:
        print(e)

def create_table(conn):
    create = """
        CREATE TABLE IF NOT EXISTS demotable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name CHAR(250) NOT NULL,
            email CHAR(250) NOT NULL,
            phone CHAR(250) NOT NULL
        );
    """
    cur=conn.cursor()
    cur.execute(create)
    print("user table was created successfully.")

def read_csv(conn):
    users = []
    with open("demo.csv","r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(user)
        return users[1:]

#2
def inser_user(conn, user_data):
    insert="""
        INSERT INTO demotable(name, email, phone) VALUES (?, ?, ?)
    """
    cur = conn.cursor()
    cur.executemany(insert,user_data)
    conn.commit()
    print(f"{len(user_data)}user table was inserted successfully")

#4 , 6
def select_users(conn,no_of_users=0):

    cur = conn.cursor()
    if no_of_users:
        users = cur.execute("SELECT * FROM demotable LIMIT ?;",(no_of_users,))
    else:
        users = cur.execute("SELECT * FROM demotable")
    for user in users:
        print(user)
#5
def select_id(conn,id):
    cur = conn.cursor()
    data =  cur.execute("SELECT * FROM demotable WHERE id =?" , (id,))
    for i in data:
        print("user found :",i)
#7 6
def delete_users(conn,id=0):
    cur = conn.cursor()
    if id > 0:
        cur.execute("DELETE FROM demotable WHERE id= ?;" ,(id,))
        conn.commit()
        print(f"deleted users whose id is {id} ")
    else:
        cur.execute("DELETE FROM demotable;")
        conn.commit()
        print(f"deleted all users")


#9
def update_user_by_id(conn, user_id,column_name,column_value):
    update_query = f"UPDATE  demotable SET {column_name} = ? where id =?"
    cur=conn.cursor()
    cur.execute(update_query,(column_value,user_id))
    conn.commit()
    print(f"{column_name} was updated with value [{column_value}] of user with id [{user_id}]")

input_string="""
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
COLUMNS =(
    "name", "email", "phone"
)

def main():
    conn= create_connection()
    user_input = input(input_string)
    if user_input == "1":
        create_table(conn)
    elif user_input == "2":
        user_data = read_csv(conn)
        inser_user(conn,user_data)
    elif user_input == "3":
        user_data = []
        for column in COLUMNS:
            col_value = input(f"Enter the value of {column}")
            user_data.append(col_value)

        inser_user(conn, [tuple(user_data)])

    elif user_input == "4":
        select_users(conn)
    elif user_input == "5":
        user_id = input("Enter user id: ")
        if user_id.isnumeric:
            select_id(conn,user_id)
    elif user_input == "6":
        no_of_users= int(input("Enter a number of users to fetch records"))
        if no_of_users > 0:
            select_users(conn,no_of_users)
    elif user_input == "7":
        conform = input("Are you sure you want to delete all user? (y/n)")
        if conform == "y":
            delete_users(conn)
    elif user_input == "8":
        id = int(input("Enter a id number to delete user"))
        if id > 0:
            conform = input(f"Are you sure you want to delete {id} user? (y/n)")
            if conform == "y":
                delete_users(conn,id)
    elif user_input == "9":
        user_id = int(input("Enter a user id: "))
        if user_id:
            select_id(conn,user_id) #calling 5 no ko metod to show details of users
            column_name = input(f"Enter the column you want to edit , please make sure column is with in {COLUMNS}")
            if column_name in COLUMNS:
                column_value = input(f"Enter the value of {column_name}")
                update_user_by_id(conn, user_id,column_name,column_value)
    elif user_input == "10":
        pass

main()