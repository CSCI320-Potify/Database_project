from src.db import *
import datetime


def add_to_collection(user):
    connection = connect()
    cursor = connection.cursor()
    while True:
        collect = input("What is the name of the collection you wish to add to?\n")
        if collect == "quit":
            break
        cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND user=%s', (collect, user))
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
                print("The specified song was not found.")
        else:
            print("The specified collection was not found.")
    connection.close()


def create_collection(user):
    connection = connect()
    cursor = connection.cursor()
    while True:
        collect = input("What is the name of the collection you wish to add?\n")
        if len(collect.strip()) != 0:
            break
        print("Collection name is invalid. Please try again.")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists == 0:
        cursor.execute('SELECT COUNT(*) FROM "collection" WHERE username=%s', (user))
        if cursor.fetchone()[0] == 0: # if user has no collections
            new_num = 0
        else:
            cursor.execute('SELECT MAX(collection_num) FROM "collection"')
            new_num = cursor.fetchone()[0] + 1    
        cursor.execute('INSERT INTO "collection" VALUES (%s, %s, %s, %s, %s)', (collect, new_num, "0", "0", user))
        connection.commit()
        print("Collection successfully created!")
    else:
        print("A collection with this name already exists!")
    connection.close()


def delete_from_collection(user):
    connection = connect()
    cursor = connection.cursor()
    collect = input("What is the name of the collection you wish to delete from?\n")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists > 0:
        song = input("What is the name of the song you wish to delete?")
        if song == "quit":
            return
        cursor.execute('SELECT song_num FROM "Song" WHERE Title=%s', ([song]))
        song_nu = cursor.fetchone()[0]
        cursor.execute('SELECT collection_num FROM "collection" WHERE name=%s AND username=%s', (collect, user))
        collect_nu = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM "collection-song" WHERE Collection_num=%s AND song_num=%s', (collect_nu, song_nu))
        song_exists = cursor.fetchone()[0]
        if song_exists > 0:
            cursor.execute('DELETE FROM "collection" WHERE name=%s AND username=%s', (collect, user))
            connection.commit()
            print("Song successfully deleted!")
        else:
            print("This song was not found.")
    else:
        print("This collection was not found.")
    connection.close()


def delete_collection(user):
    connection = connect()
    cursor = connection.cursor()
    collect = input("What is the name of the collection you wish to delete?\n")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists > 0:
        cursor.execute('DELETE FROM "collection" WHERE name=%s AND username=%s', (collect, user))
        connection.commit()
        print("Collection successfully deleted!")
    else:
        print("This collection was not found.")
    connection.close()


def play_collection(user):
    connection = connect()
    cursor = connection.cursor()
    collect = input("What is the name of the collection you wish to play?\n")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists > 0:
        cursor.execute('SELECT collection_num FROM "collection" WHERE name=%s AND username=%s', (collect, user))
        coll_num = cursor.fetchone()[0]
        cursor.execute('UPDATE "collection-song" SET played=%s WHERE collection_num=%s', (True, coll_num))
        connection.commit()
        print("Playing collection...")
    else:
        print("This collection was not found.")
    connection.close()


def rename_collection(user):
    connection = connect()
    cursor = connection.cursor()
    collect = input("What is the name of the collection you wish to rename?\n")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists > 0:
        rename = input("What is the new name you wish to give it?\n")
        if rename == "quit":
            return
        cursor.execute('UPDATE "collection" SET name=%s WHERE name=%s AND username=%s', (rename, collect, user))
        connection.commit()
        print("Collection successfully renamed!")
    else:
        print("This collection was not found.")
    connection.close()


def view_collections(user):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "collection" WHERE username=%s ORDER BY name ASC', ([user]))
    all_collections = cursor.fetchone()
    print(all_collections)
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
            play_collection(user)
        elif choice == "6":
            rename_collection(user)
        elif choice == "7":
            view_collections(user)
        elif choice == "8":
            break
        else:
            print("Unknown command")


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
                    print("You are no longer following " + found_user[0])
    connection.close()
    print("Returning to options select")



def searchSong():
    return
    

def populateTestData():
    sql_query = os.path.join(os.path.dirname(__file__), f'sample_queries.sql')
    connection = connect()
    cursor = connection.cursor()
    with open(sql_query, 'r') as file:
        cursor.execute(file.read())
    connection.commit()
    connection.close()

