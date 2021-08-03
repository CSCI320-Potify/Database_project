from src.db import *
from src.search_help import *

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


"""
Search for song by title, artist, album, or genre
"""
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
            num = searchForSong("title")
        elif choice == '1':
            num = searchForSong("artist")
        elif choice == '2':
            num = searchForSong("album")
        elif choice == '3':
            num = searchForSong("genre") 
        elif choice == '9':
            return
        else:
            print("Invalid command. Try again.")
        return num

"""
Searches for songs based on what the user has input.
Search for genre looks for songs that have any of the inputted genres.
that includes the input. 
"""
def searchForSong(term):
    search = searchConditions(term)
    if search == "NULL":
        return "NULL"

    connection = connect()
    cursor = connection.cursor()

    if term == "title":
        cursor.execute('SELECT "song_num" FROM "song" WHERE "Title" LIKE %s', ([search]))

    elif term == "artist":
        cursor.execute('SELECT "artist_num" FROM "artist" WHERE "name" LIKE %s', ([search]))
        artist_num = cursor.fetchall()
        cursor.execute('SELECT "song_num" FROM "artist-song" WHERE "artist_num" = ANY(%s)', (artist_num,))

    elif term == "album":
        cursor.execute('SELECT "album_num" FROM "album" WHERE "name" LIKE %s', ([search]))
        album_num = cursor.fetchall()
        cursor.execute('SELECT "song_num" FROM "song-album" WHERE "album_num" = ANY(%s)', (album_num,))
       
    elif term == "genre": 
        cursor.execute('SELECT "genre_list_id" FROM "genre-genre_list" WHERE "genre_id" = ANY(%s)', (search,))
        genre_list_id = cursor.fetchall()
        cursor.execute('SELECT "song_num" FROM "song-genre" WHERE "genre_list" = ANY(%s)', (genre_list_id,))

    song_num = cursor.fetchall()
    return displayPages(song_num)

    connection.close()


"""
Private. Songs will only be displayed in pages of 10 or less songs.
User can only go forward in pages, but not backwards.
"""
def displayPages(song_num):
    sort = sortByVerification()
    order = getSongOrder(sort, song_num)

    if len(order) == 0:
        print("No results")
        return
    
    pages = int(len(order) / 10)
    song_ptr = 0
    for page in range(pages + 1):
        songs, song_ptr, song_list = getTenSongs(order, song_ptr)
        print("Page", str(page))
        print("Title, Artist, Album, Length, Listen Count") 
        count = 0
        for song in songs.values(): 
            min, sec = divmod(song[3], 60000)
            time = "{:02d}:{:02d}".format(min, int(sec / 1000))
            print(song_ptr)
            print(str(count) + f": {song[0]}, {song[1]}, {song[2]}, {time}, {song[4]}") 
            count += 1


        while True:
            print("Select song [0-9] to add to collection")
            choice = input()
            if page != pages:
                print("Next page? (y|n)")  
                if choice == 'n':
                    return
                elif choice == 'y':
                    break
            choice = int(choice)
            if choice >= 0 & choice < 10:
                song_num = song_list[choice]
                return song_num
            else:
                print("Invalid option. Try again.")
    return