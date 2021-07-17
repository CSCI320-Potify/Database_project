"""
Signup and signin
"""

from src.db import *
import datetime

"""
Creates a new user. User will have a unique username and email. 
A new account will have a password, first name, last name, creation date,
and last access date

"""
def signup():
    # initial sign up process needs credentials to be of certain requirements
    connection = connect()
    cursor = connection.cursor()
    
    while True:
        first_name = input("Enter First Name:\n")
        if len(first_name.strip()) == 0:
            print("First name is invalid. Please try again.")
        else:
            break
    while True:
        last_name = input("Enter Last Name:\n")
        if len(last_name.strip()) == 0:
            print("Last name is invalid. Please try again.")
        else:
            break
    while True:
        username = input("Enter Username:\n")
        cursor.execute('SELECT COUNT(username) FROM "user" WHERE username=%s', ([username]))
        if cursor.fetchone()[0] != 0:
            print("Username is already taken. Please try again")
        elif len(username.strip()) == 0: 
            print("Username is invalid. Please try again")
        else:
            break
    
    password = input("Enter Password:\n") # I'm going to make it so having a password is a choice for now

    while True:
        email = input("Enter Email:\n")
        cursor.execute('SELECT COUNT(email) FROM "user" WHERE email=%s', ([email]))
        if '@' not in email:         
            print("Email is invalid. Please try again.")
        elif cursor.fetchone()[0] != 0:
            print("Email is already taken. Please try again.")
        else:
            break
    now = datetime.datetime.utcnow()
    
    cursor.execute(
        'INSERT INTO "user"(username, password, email, first_name, last_name, creation_date, last_access_date) VALUES (%s, %s, %s, %s, %s, %s, %s)',
        (username, password, email, first_name, last_name, now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
    connection.commit()
    connection.close()
    return username


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