from src.db import *
import datetime

def signup():
    first_name = input("Enter First Name:\n")
    last_name = input("Enter Last Name:\n")
    username = input("Enter Username:\n")
    password = input("Enter Password:\n")
    email = input("Enter Email:\n")
    now = datetime.datetime.utcnow()
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(username) FROM "user" WHERE username=%s', ([username]))
    result = cursor.fetchone()[0]
    print(result)
    if result == 0:
        cursor.execute(
            'INSERT INTO "user"(username, password, email, first_name, last_name, creation_date, last_access_date) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (username, password, email, first_name, last_name, now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
        connection.close()
        return username
    connection.close()
    print("New Account Creation Failed")
    print("Username Already Exists")
    return ''


def login():
    username = input("Enter username:\n")
    password = input("Enter password:\n")
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(username) FROM "user" WHERE username=%s AND password=%s',
                (username, password))
    if cursor.fetchone()[0] == 1:
        cursor.execute('UPDATE "user" SET last_access_date=CURRENT_TIMESTAMP WHERE username=%s', ([username]))
        return username
    print("Login Unsuccessful")
    print("Username or Password incorrect")
    return ''

def show():
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            print(table)

        cursor.execute('DESC "user"')
        for column in cursor.fetchall():
            print(column)

        connection.close()
    except :
        print("failed")
        connection.close()