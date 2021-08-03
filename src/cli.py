from src.search_help import showSongs
from src.search import displayPages, searchSong
from src.db import *
import datetime

"""
Finds collection if a user has a collection and returns its collection id
"""
def find_collection(user, action):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE username=%s', ([user]))
    if cursor.fetchone()[0] == 0:
        print("There are no collections. Create a collection first.")
        connection.close()
        return "NULL"
    while True:
        if action == "delete":
            cursor.execute('SELECT "name", collection_num FROM "collection" WHERE username=%s AND "num_of_songs" > 0', ([user]))
        else:
            cursor.execute('SELECT "name", collection_num FROM "collection" WHERE username=%s', ([user]))
        collection = cursor.fetchall()
        connection.close()
        for i in range(len(collection)):
            print(str(i) + ": " + str(collection[i][0]))
        choice = input("Select collection [0-" + str(len(collection) - 1) + "] you want to " + action + "\n")
        choice = int(choice)
        if choice >= 0 & choice < len(collection):
            collection_id = collection[choice][1]
            return collection_id

"""
Searches for song to add to collection. 
Fails if the user doesn't have a collection or if the song already exists in collection.
"""
def add_to_collection(user):
    collection_id = find_collection(user, "add to")
    if collection_id != "NULL":
        song_num = searchSong()
        if song_num == "NULL":
            return
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT("song_num") FROM "collection-song" WHERE "Collection_num"=%s AND "song_num"=%s', (collection_id, song_num))
        song_exists = cursor.fetchone()[0]
        cursor.execute('SELECT "Title" FROM "song" WHERE "song_num" = %s', ([song_num]))
        title = cursor.fetchone()[0]
        cursor.execute('SELECT "name" FROM "collection" WHERE "collection_num" = %s', ([collection_id]))
        collection_name = cursor.fetchone()[0]
        if song_exists == 0:
            cursor.execute('SELECT length, "Title" FROM "song" WHERE "song_num"=%s', ([song_num]))
            length = cursor.fetchone()[0]
            cursor.execute('INSERT INTO "collection-song"("Collection_num", "song_num") VALUES (%s, %s)', (collection_id, song_num))
            connection.commit()
            cursor.execute('UPDATE "collection" SET duration = duration + %s WHERE "collection_num" = %s', (length, collection_id))
            connection.commit()
            cursor.execute('UPDATE "collection" SET num_of_songs = num_of_songs + 1 WHERE "collection_num" = %s', ([collection_id]))
            print(title, "added to collection", collection_name)
            connection.commit()
        else:
            print(title, "is already in collection", collection_name)
    connection.close()


"""
A collection is created by a certain user. A created collection cannot have the same name
as a currently existing collection under the same user. 
The name of the collection has to be lower than 19 characters
and the user cannot have more than 99 collections.
"""
def create_collection(user):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT (*) FROM "collection" WHERE username=%s', ([user]))
    if cursor.fetchone()[0] > 99:
        print("You have hit the max collections of 99. Delete to add more.")
    else:
        while True:
            collect = input("What is the name of the collection you wish to add?\n")
            if len(collect.strip()) == 0:
                print("Collection name is invalid. Please try again.")    
            elif len(collect.strip()) > 19:
                print("Collection name is too long - needs to be less than 19. Try again.")
            else: 
                break
        if collect == "quit":
            return
        cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
        exists = cursor.fetchone()[0]
        if exists == 0:
            cursor.execute('SELECT COUNT(*) FROM "collection"')
            if cursor.fetchone()[0] == 0: # if there are no collections
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


def delete_from_collection(user): # TODO
    connection = connect()
    cursor = connection.cursor()
    collection_id = find_collection(user, "delete")
    if collection_id != "NULL":
        cursor.execute('SELECT "song_num" FROM "collection-song" WHERE "Collection_num" = %s', ([collection_id]))
        song_nums = cursor.fetchall()
        song_num = displayPages(song_nums, "delete song")
        
        cursor.execute('SELECT "Title" FROM "song" WHERE "song_num" = %s', ([song_num]))
        title = cursor.fetchone()[0]
        cursor.execute('SELECT "name" FROM "collection" WHERE "collection_num" = %s', ([collection_id]))
        collection_name = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM "collection-song" WHERE "Collection_num"=%s AND song_num=%s', (collection_id, song_num))
        song_exists = cursor.fetchone()[0]
        if song_exists > 0:
            cursor.execute('SELECT length FROM "song" WHERE "song_num"=%s', ([song_num]))
            length = cursor.fetchone()[0]
            cursor.execute('DELETE FROM "collection-song" WHERE "Collection_num"=%s AND song_num=%s', (collection_id, song_num))
            connection.commit()
            cursor.execute('UPDATE "collection" SET duration = duration - %s WHERE "collection_num" = %s', (length, collection_id))
            connection.commit()
            cursor.execute('UPDATE "collection" SET num_of_songs = num_of_songs - 1 WHERE "collection_num" = %s', ([collection_id]))
            connection.commit()
            print(title, "successfully deleted!")
        else:
            print(title, "was not found in collection", collection_name)

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
        cursor.execute('SELECT song_num FROM "collection-song" WHERE "Collection_num"=%s', ([coll_num]))
        songs = cursor.fetchall()
        for s in songs:
            cursor.execute('SELECT COUNT(*) FROM "user-song" WHERE username=%s AND song_num=%s', (user, s))
            user_played = cursor.fetchone()[0]
            if user_played:
                cursor.execute('UPDATE "user-song" SET play_count=play_count+1 WHERE username=%s AND song_num=%s', (user, s))
                connection.commit()
            else:
                cursor.execute('INSERT INTO "user-song" VALUES (%s, %s, %s)', (user, s, 1))
        connection.commit()
        print("Playing collection...")
    else:
        print("This collection was not found.")
    connection.close()

"""
Renamed collections cannot be greater than 19 characters
and contain the same name as a pre-existing collection under the same user
"""
def rename_collection(user):
    connection = connect()
    cursor = connection.cursor()
    collect = input("What is the name of the collection you wish to rename?\n")
    if collect == "quit":
        return
    cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (collect, user))
    exists = cursor.fetchone()[0]
    if exists > 0:
        while True:
            rename = input("What is the new name you wish to give it?\n")
            cursor.execute('SELECT COUNT(*) FROM "collection" WHERE name=%s AND username=%s', (rename, user))
            if len(rename.strip()) == 0:
                print("Invalid name. Please try again.")
            elif len(rename.strip()) > 19:
                print("New name is too long - must be less than 19 characters. Try again.")
            elif cursor.fetchone()[0] == 1:
                print("Collection of", rename, "already exists. Choose another name.")
            else:
                break
        if rename == "quit":
            return
        cursor.execute('UPDATE "collection" SET name=%s WHERE name=%s AND username=%s', (rename, collect, user))
        connection.commit()
        print("Collection successfully renamed!")
    else:
        print("This collection was not found.")
    connection.close()

"""
Prints view of collection in the following format:

ID name                length  number_of_songs
---------------------------------------------

id cannot exceed 99 and name cannot be of length greater than 19

"""
def view_collections(user):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "collection" WHERE username=%s ORDER BY name ASC', ([user]))
    all_collections = cursor.fetchall()
    print("{:<3}{:<20}{:<10}{:<6}".format("id", "name", "length", "num_of_songs" ))
    print("-" * 45)
    if len(all_collections) == 0:
        print("<No collections>")
    else:
        for collection in all_collections:
            min, sec = divmod(collection[2], 60000)
            hour, min = divmod(min, 60)
            time = "{:d}:{:02d}:{:02d}".format(hour, min, int(sec / 1000))
            print("{:^3}{:<20}{:<10}{:<6}".format(collection[1], collection[0], time, collection[3]))
    connection.close()


def collections(user):
    while True:
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

def Recommendation(user):
    print("1: Top 50 most popular songs in the last 30 days")
    print("2: Top 50 most popular songs among my friends")
    print("3: Top 5 most popular genres of the month")
    print("4: For you: Recommendations")
    print("5: Go Back")

    while True:
        choice = input()
        connection = connect()
        cursor = connection.cursor()
        if choice == 1:
            cursor.execute('SELECT song.song_num FROM "user-song" Inner join song on song.song_num = "user-song".song_num group by song.song_num order by sum(play_count)')
            global_rec = cursor.fetchall();
            print("Top 50 songs")
            for i in range(50):
                print("%s, Title: %s",i,global_rec[i])
            pass
        elif choice == 2: #pop among friends
            cursor.execute('Select song_num, play_count from "user-song" INNER JOIN friends on "user-song".username = friends.follows where friends.user = %s GROUP BY song_num ORDER BY sum(play_count)', ([user]))
            friend_rec = cursor.fetchall();
            print("Top 50 songs among friends")
            for i in range(50):
                print("%s, Title: %s",i,friend_rec[i])
            # TODO remove play_count after testing

            pass
        elif choice == 3: #genre of the month
            '''SELECT genre.name
from genre natural join "genre-genre_list" "g-gl" on genre.id = "g-gl".genre_id natural join "genre_list" "gl" on genre_list_id = "gl".genre_list_id natural join "user-song" on song_num  natural join song s on "user-song".song_num = s.song_num
GROUP BY song_num
order by SUM(play_count)'''
            pass
        elif choice == 4: #Rec

            pass
        elif choice == 5: #Go back
            break

def populateTestData():
    sql_query = os.path.join(os.path.dirname(__file__), f'sample_queries.sql')
    connection = connect()
    cursor = connection.cursor()
    with open(sql_query, 'r') as file:
        cursor.execute(file.read())
    # connection.commit()
    connection.close()

