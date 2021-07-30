from src.db import *
from re import compile, search

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
@param sort determines how the songs are sorted in the page results
either by title, artist, genre, or release date ascending or descending

@return the order that songs will be displayed
"""
def getSongOrder(sort, song_num):
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

    return order


"""
Will return a dictonary up to 10 songs.
song_num : (title, artist, album, length, play_count)
"""
def getTenSongs(order, song_ptr):
    songs = {}

    connection = connect()
    cursor = connection.cursor()
    order = order[song_ptr:]
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
        song_ptr += 1
        if song_ptr % 10 == 0:
            break


    connection.close()

    return songs, song_ptr


