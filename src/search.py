from src.db import *
from re import compile, search

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
        search = input().strip()
        if search == "q!":
            return "NULL"
        elif len(search.strip()) < 3:
            print("Please enter 3 or more characters.")
        else:
            search = '%' + search + '%'
            break
    return search

"""
@param sort determines how the songs are sorted in the page results
either by title, artist, genre, or release date ascending or descending
songs will be stored in a dictionary:
song_num: (title, artist, album, release_date, listen_count)

@return song's name, artist name, album, length, and listen count
"""
def sortBy(sort, song_num):
    songs = {}

    orderby = "Title"
    descending = False

    connection = connect()
    cursor = connection.cursor()

    if len(sort) > 0:
        method = sort[0]
        if sort[-1] == 'd':
            descending = True
        if method == 0:
            orderby = "artist"
        elif method == 1:
            orderby = "genre"
        elif method == 2:
            orderby = "release_date"

    cursor.execute('SELECT song_num FROM "song" WHERE "song_num" = ANY(%s) ORDER BY %s', (song_num, [orderby]))
    order = [r[0] for r in cursor.fetchall()]

    if descending == True:
        order.reverse()
    
    for song_num in order:
        cursor.execute(f'SELECT "Title", "length" FROM "song" WHERE "song_num" = {song_num}')
        title, length = cursor.fetchone()

        # artist name
        cursor.execute(f'SELECT artist_num FROM "artist-song" WHERE "song_num" = {song_num}')        
        artist_num = cursor.fetchone()[0]
        cursor.execute(f'SELECT name FROM "artist" WHERE "artist_num" = {artist_num}')
        artist_name = cursor.fetchone()[0]

        # album name
        cursor.execute(f'SELECT album_num FROM "song-album" WHERE "song_num" = {song_num}')
        album_num = cursor.fetchone()[0]
        cursor.execute(f'SELECT name FROM "album" WHERE "album_num" = {album_num}')
        album_name = cursor.fetchone()[0]

        # play count
        cursor.execute(f'SELECT play_count FROM "user-song" WHERE "song_num" = {song_num}')
        temp = cursor.fetchone()
        if temp is None:
            play_count = 0
        else:
            play_count = temp[0]

        song = (title, artist_name, album_name, length, play_count)
        songs[song_num] = song

    connection.close()
    
    return songs, order
    

"""
Private. Songs will only be displayed in pages of 10 or less songs.
User can only go forward in pages, but not backwards.
"""
def displayPages(song_num):
    sort = sortByVerification()
    songs, order = sortBy(sort, song_num)

    if len(songs) == 0:
        print("No results")
        return
    
    pages = int(len(songs) / 10)
    song_ptr = 0
    for page in range(pages + 1):
        print("Page", str(page))
        print("{:<10}{:<10}{:<10}{:<5}{:<6}".format("Title", "Artist", "Album", "Release Date", "Play Count"))
        print("-" * 43)
        for num in order: # TODO formatting based on DB and other tables
            print(songs.get(num))
            #print("{:<10}{:<10}{:<10}{:<5}{:<6}".format(songs
            #song_ptr += 1
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
Validifies the method of sorting song. (0 | 1 | 2) & (d |  )
"""
def sortByVerification():
    while True:
        print("Sort by (default alphabetically by title): [artist(0) | genre(1) | release year(2)] | [descending(d)]")
        sort = input().strip()
        regexp = compile(r"(0|1|2| )?(d| )?")
        if regexp.search(sort) != None:
            return sort
        print("Invalid command.")

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
        cursor.execute('SELECT "song_num" FROM "song" WHERE "Title" LIKE %s', ([search]))

    elif term == "artist":
        cursor.execute('SELECT "artist_num" FROM "artist" WHERE "name" LIKE %s', ([search]))
        artist_num = cursor.fetchall()
        cursor.execute(f'SELECT "song_num" FROM "artist_song" WHERE "artist_num" IN {artist_num}')

    elif term == "album":
        cursor.execute('SELECT "album_num" FROM "album" WHERE "name" LIKE %s', ([search]))
        album_num = cursor.fetchall()
        cursor.execute(f'SELECT "song_num" FROM "song-album" WHERE "album_num" IN {album_num}')
       
    elif term == "genre": # TODO
        """
        while True:
            print("Enter in a genre:")
            genres = input().strip()
            if len(genres) == 0:
                print("Enter at least one genre")
            else:
                break
        cursor.execute('SELECT "song_num" FROM "song-genre" WHERE "genre_list" LIKE ')
        """

    song_num = cursor.fetchall()
    displayPages(song_num)

    connection.close()