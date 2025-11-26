from apl import register_user, login_user

# Display menu
def menu():
    print("1. Register")
    print("2. Login")   
    print("3. Exit")

# Main function
def main():
    while True:
        menu()
        choice = input("Enter choice: ")
        if choice == "1":
            register_user()
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)
        elif choice == "3":
            print("Exiting...")
            break



import sqlite3

conn = sqlite3.connect('Data/intelligence_platform.db')
curr = conn.cursor()
sql = (""" INSERT INTO users (username, password_hash) VALUES (?, ?) """)
param =('alice', 'hashed_password_123',)
curr.execute(sql,param)
conn.commit()
conn.close

def add_user(conn, name, hash):
    curr = conn.cursor()
    sql =(""" INSERT INTO users  (username, password_hash) VALUES (?, ?) """)
    param =(name,hash)
    curr.execute(sql, param)
    conn.commit()
    conn.close()

def get_users():
    curr = conn.cursor()
    sql = ("""SELECT * FROM USERS""")
    curr.execute(sql)
    users = curr.fetchall()
    conn.close()
    return users

def migrate_users():
    with open('user.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn, name, hash)
    conn.close()

