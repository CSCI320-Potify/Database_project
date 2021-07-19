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
        4: Go back
        ''')
        choice = input()
        # TODO plans for function reusability
        if choice == '0':
            searchSongTitle()
        elif choice == '1':
            searchSongArtist()
        elif choice == '2':
            searchSongAlbum()
        elif choice == '3':
            searchSongGenre()
        elif choice == '4':
            break
        else:
            print("Invalid command. Try again.")

"""
Song search by title will take 3 or more characters as input and finds all songs
that includes the input. 
"""
def searchSongTitle():
    while True:
        print("Enter song title (3 or more characters) | 'q!' to go back: ")
        title = input()
        if len(title.strip()) < 3:
            print("Please enter 3 or more characters.")
        elif title == "q!":
            return
        else:
            title = '%' + title + '%'
            break
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM "song" WHERE "Title" LIKE %s', ([title]))
    songs = cursor.fetchall()
    pages = int(len(songs) / 10)
    for page in range(pages + 1):
        print("Page", str(page))
        for song in songs: # TODO formatting based on DB
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
    connection.close()