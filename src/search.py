from src.db import *

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
    while True:
        print('''Search song by:
        0: Title
        1: Artist
        2: Album
        3: Genre
        9: Go back
        ''')
        choice = input()
        if choice == '0':
            searchForSong("title")
        elif choice == '1':
            searchForSong("artist")
        elif choice == '2':
            searchForSong("album")
        elif choice == '3':
            searchForSong("genre") # TODO 
        elif choice == '9':
            return
        else:
            print("Invalid command. Try again.")

"""
Private. Ensures that a search term is 3 or more characters long before
a song can be searched for. 
The term has no trailing white space and is a substring
"""
def searchConditions(term):
    while True:
        print(f"Enter song {term} (3 or more characters) | 'q!' to go back: ")
        search = input()
        if len(search.strip()) < 3:
            print("Please enter 3 or more characters.")
        elif search == "q!":
            return "NULL"
        else:
            search = '%' + search + '%'
            break
    return search

"""
Private. Songs will only be displayed in pages of 10 or less songs.
User can only go forward in pages, but not backwards.
"""
def displayPages(songs):
    if len(songs) == 0:
        print("No results")
        return
    pages = int(len(songs) / 10)
    for page in range(pages + 1):
        print("Page", str(page))
        for song in songs: # TODO formatting based on DB and other tables
            """   
            """
            print(song)
        if page != pages: # last page
            while True:
                print("Next page? (y|n)")
                choice = input()
                if choice == 'n':
                    return
                elif choice == 'y':
                    break
                else:
                    print("Invalid option. Try again.")

"""
Song search by title will take 3 or more characters as input and finds all songs
that includes the input. 
"""
def searchForSong(term):
    search = searchConditions(term)
    if search == "NULL":
        return

    connection = connect()
    cursor = connection.cursor()

    if term == "title":
        cursor.execute('SELECT * FROM "song" WHERE "Title" LIKE %s', ([search]))
        songs = cursor.fetchall()
        
    elif term == "artist":
        cursor.execute('SELECT "artist_num" FROM "artist" WHERE "name" LIKE %s', ([search]))
        artist_num = cursor.fetchall()
        songs = []
        for num in artist_num:
            cursor.execute('SELECT "song_num" FROM "artist_song" WHERE "artist_num"=%s', ([num]))
            song_num = cursor.fetchone()[0]
            cursor.execute('SELECT * FROM "song" WHERE "song_num"=%s', ([song_num]))
            songs.append(cursor.fetchone()[0])
    elif term == "album":
        cursor.execute('SELECT "album_num" FROM "album" WHERE "name" LIKE %s', ([search]))
        album_num = cursor.fetchall()
        songs = []
        for num in album_num:
            cursor.execute('SELECT "song_num" FROM "song-album" WHERE "album_num"=%s', ([num]))
            song_num = cursor.fetchone()[0]
            cursor.execute('SELECT * FROM "song" WHERE "song_num"=%s', ([song_num]))
            songs.append(cursor.fetchone()[0])
    elif term == "genre":
        pass

    displayPages(songs)

    connection.close()