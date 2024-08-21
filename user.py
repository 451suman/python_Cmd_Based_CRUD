import sqlite3
def create_connection():
    try:
        con=sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print(f"error:{e}")
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
#1
def create_table(conn):
    CREATE_USERS_TABLE_QUERY="""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name CHAR(255) NOT NULL,
    last_name CHAR(255) NOT NULL,
    company_name CHAR(255) NOT NULL,
    address CHAR(255) NOT NULL,
    city CHAR(255) NOT NULL,
    county CHAR(255) NOT NULL,
    state CHAR(255) NOT NULL,
    zip REAL NOT NULL,
    phone1 CHAR(255) NOT NULL,
    phone2 CHAR(255) NOT NULL,
    email CHAR(255) NOT NULL,
    web text);"""
    cur=conn.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("user table was created successfully.")

import csv
#2
def read_csv():
    users=[]
    with open("sample_users.csv","r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))
        return users[1:]


#2
#3
def insert_users(con,users):
    user_add_query="""
        INSERT INTO users(
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone2,
            email,
            web)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"""
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)} users were imported successfully.")



#5
def select_user_by_id(con,user_id):
    cur=con.cursor()
    users=cur.execute(f"SELECT * FROM users where id=?;",(user_id,))
    for user in users:
        print(user)

#4
#6
def select_user(con,no_of_user=0):
    cur=con.cursor()
    if no_of_user:  #6 
        users = cur.execute("SELECT * FROM users LIMIT ?",(no_of_user,))

    else: #if user = 0 else part is run #4
        users = cur.execute("SELECT * FROM users")

    for user in users:
        print(user)


#7
def delete_all_users(conn):
    cur= conn.cursor()
    cur.execute("DELETE FROM users;")
    conn.commit()
    print("deleted all users")

#8
def delete_user_id(conn, id):
    cur= conn.cursor()
    cur.execute("DELETE FROM users WHERE id= ? ;",(id,))
    conn.commit()
    print(f"{id} user deleted")

COLUMNS=(
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web"
)

#9
def update_user_by_id(conn, user_id,column_name,column_value):
    update_query = f"UPDATE  users SET {column_name} = ? where id =?"
    cur=conn.cursor()
    cur.execute(update_query,(column_value,user_id))
    conn.commit()
    print(f"{column_name} was updated with value [{column_value}] of user with id [{user_id}]")


def main():
    conn=create_connection()
    user_input=input(INPUT_STRING)
    if user_input == "1":
        create_table(conn)
    elif user_input == "2":
       users_data =  read_csv()
       insert_users(conn,users_data)
    elif user_input == "3":
        data = []
        for column in COLUMNS:
            col_value = input(f"enter the value of {column}: ")
            data.append(col_value)
        # print([tuple(data)])
        insert_users(conn,[tuple(data)])   #use old insert function 
        #[(a,a,a,aa,asd,asd,)]

    elif user_input == "4":
        select_user(conn)
    elif user_input == "5":
        user_id = input("Enter user id: ")
        if user_id.isnumeric:
            select_user_by_id(conn,user_id)
    elif user_input == "6":
        no_of_users = input("Enter a number of users to fetch records: ")
        if no_of_users.isnumeric() and int(no_of_users) > 0:
            select_user(conn, int(no_of_users))
    elif user_input == "7":
        conform = input("Are you sure you want to delete all users? (y/n): ")
        if conform == "y":
            delete_all_users(conn)
    elif user_input == "8":
        id=int(input("Enter a id to delete: "))
        conform = input(f"Are you sure you want to delete this id {id} user? (y/n): ")
        if conform == "y":
            delete_user_id(conn, id)

    elif user_input == "9":
        user_id = int(input("Enter a id of user: "))
        if user_id:
            select_user_by_id(conn,user_id)
            column_name = input(f"Enter the column you want to edit, please make sure column is with in {COLUMNS}")
            if column_name in COLUMNS:
                column_value = input(f"Enter the value of {column_name}")
                update_user_by_id(conn, user_id,column_name,column_value)
    elif user_input == "10":
        pass
        
main()