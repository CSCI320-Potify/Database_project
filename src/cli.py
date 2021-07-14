from src.db import *
import datetime


def add_to_collection():
    connection = connect()
    cursor = connection.cursor()
    while True:
        collect = input("What is the name of the collection you wish to add to?\n")
        if collect == "quit":
            break
        cursor.execute('SELECT COUNT(name) FROM "collection" WHERE name=%s', ([collect]))
        find_col = cursor.fetchone()[0]
        if find_col == 1:
            song = input("What is the name of the song you wish to add to " + collect + "?\n")
            if song == "quit":
                break
            cursor.execute('SELECT COUNT(Title) FROM "Song" WHERE Title=%s', ([song]))
            find_song = cursor.fetchone()[0]
            if find_song == 1:
                cursor.execute('INSERT INTO "collection-song"(Collection_num, song_num) VALUES (1, 2)')
                connection.commit()
            else:
                print("The specified song was not found")
        else:
            print("The specified collection was not found")
    connection.close()


def create_collection(user):
    connection = connect()
    cursor = connection.cursor()
    collect = input("What is the name of the collection you wish to add?\n")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists == 0:
        cursor.execute('SELECT MAX(collection_num) FROM "collection"')
        new_num = cursor.fetchone()[0] + 1
        cursor.execute('INSERT INTO "collection" VALUES (%s, %s, %s, %s, %s)', (collect, new_num, "0", "0", user))
        connection.commit()
        print("Collection successfully added!")
    else:
        print("A collection with this name already exists!")
    connection.close()


def collections(user):
    while True:
        print("Hello " + user)
        print("Select one of the following options")
        print("1: Add to collection")
        print("2: Create new collection")
        print("3: Delete from collection")
        print("4: Delete a collection")
        print("5: Play a collection")
        print("6: Rename a collection")
        print("7: View all collections")
        print("8: Go back")
        choice = input()

        if choice == "1":
            add_to_collection(user)
        elif choice == "2":
            create_collection(user)
        elif choice == "3":
            delete_from_collection(user)
        elif choice == "4":
            delete_collection(user)
        elif choice == "5":
            play_collection()
        elif choice == "6":
            rename_collection()
        elif choice == "7":
            view_collections()
        elif choice == "8":
            break
        else:
            print("Unknown command")


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