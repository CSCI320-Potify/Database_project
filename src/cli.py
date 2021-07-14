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

def searchUser(current_user):
    email = input("Enter email of user to search for:")
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT username, email from "user" WHERE email=%s', [email])
    found_user = cursor.fetchone()
    if found_user is None:
        print("User Not Found")
    else:
        print("Email has user " + found_user[0] + " associated with it")
        if current_user == found_user[0]:
            print("User searched is same as current user")
        else:
            cursor.execute('SELECT COUNT(*) FROM "friends" WHERE "user"=%s AND follows=%s',
                (current_user, found_user[0]))
            following = cursor.fetchone()[0]
            if following == 0:
                print("You are not currently following this user, would you like to follow?")
                select = input("1 for yes, 2 for No: ")
                if select == '1':
                    cursor.execute('INSERT INTO "friends" VALUES (%s,%s)', (current_user, found_user[0]))
                    connection.commit()
                    print("You are now following " + found_user[0])
            else:
                print("You are already following this user, would you like to unfollow?")
                select = input("1 for yes, 2 for No: ")
                if select == '1':
                    cursor.execute('DELETE FROM "friends" WHERE  "user"=%s AND follows=%s', (current_user, found_user[0]))
                    connection.commit()
                    print("You are no longer following" + found_user[0])
    connection.close()
    print("Returning to options select")