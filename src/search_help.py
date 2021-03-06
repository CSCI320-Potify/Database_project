from src.db import *
from re import compile, search

"""
Private. For title, artist, and album, ensure that a search term is 3 or more characters long before
a song can be searched for. 
If genre, then user can search for multiple valid genres
The term has no trailing white space and is a substring
"""
def searchConditions(term):
    while True:
        if term == "genre":
            connection = connect()
            cursor = connection.cursor()
            genre_list = []
            while True:
                print("Enter in a genre. Press <enter> to add genre. '!q' to finish")
                genre = input().strip()
                if genre == "!q":
                    if len(genre_list) == 0:
                        return "NULL"
                    return genre_list
                cursor.execute('SELECT "id" FROM "genre" WHERE "name" LIKE %s', ([genre]))
                genre_id = cursor.fetchone()
                if genre_id is None:
                    print("Genre doesn't exist. Try again")
                else:
                    genre_list.append(genre_id[0])
        else:
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
Artist name is sorted alphabetically descending or ascending
Genre is sorted by genre_id descending or ascending
"""
def getArtistGenreOrder(song_num, method, descending):
    connection = connect()
    cursor = connection.cursor()

    if method == '0': # artist
        cursor.execute('SELECT "artist_num" FROM "artist-song" WHERE "song_num" = ANY(%s)', (song_num,))
        artist_num = cursor.fetchall()
        cursor.execute('SELECT "name" FROM "artist" WHERE "artist_num" = ANY(%s) ORDER BY "name"' , (artist_num,))
        artist = cursor.fetchall()
        cursor.execute('SELECT "artist_num" FROM "artist" WHERE "name" = ANY(%s) ORDER BY "name"', (artist,))
        artist_num = cursor.fetchall()
        order = []
        for num in artist_num:
            cursor.execute('SELECT "song_num" FROM "artist-song" WHERE "artist_num" = %s AND "song_num" = ANY(%s)', 
            (num, song_num))
            order.append(cursor.fetchone()[0])
    elif method == '1': # genre
        cursor.execute('SELECT "genre_list" FROM "song-genre" WHERE "song_num" = ANY(%s)', (song_num,))
        genre_list_id = cursor.fetchall()
        cursor.execute('SELECT "genre_id", "genre_list_id" FROM "genre-genre_list" WHERE "genre_list_id" = ANY(%s) ORDER BY "genre_id"', 
        [genre_list_id])
        genre_id = cursor.fetchall()
        order = []
        for genre, id in genre_id:
            cursor.execute('SELECT "song_num" FROM "song-genre" WHERE "genre_list" = %s', [id])
            order.append(cursor.fetchone()[0])
        order = list(dict.fromkeys(order))

    connection.close()
    
    if descending == True:
        order.reverse()
    
    return order

    
"""
@param sort determines how the songs are sorted in the page results
either by title, artist, genre, or release date ascending or descending

@return the order that songs will be displayed
"""
def getSongOrder(sort, song_num):
    descending = False

    connection = connect()
    cursor = connection.cursor()

    print("Obtaining order...")
    if len(sort) > 0:
        method = sort[0]
        
        if sort[-1] == 'd':
            descending = True
        if int(method == '0') | int(method == '1'): # artist and genre
            return getArtistGenreOrder(song_num, method, descending)
        elif method == '2': # release_date
            cursor.execute('SELECT "song_num" FROM "song" WHERE "song_num" = ANY(%s) ORDER BY "release_date"', (song_num,))
        else:
            cursor.execute('SELECT "song_num" FROM "song" WHERE "song_num" = ANY(%s) ORDER BY "Title"', (song_num,))
    else:
        cursor.execute('SELECT "song_num" FROM "song" WHERE "song_num" = ANY(%s) ORDER BY "Title"', (song_num,))
    print("Order obtained.")

    order = [r[0] for r in cursor.fetchall()]

    connection.close()

    if descending == True:
        order.reverse()

    return order

"""
Prints out the songs in order
@param order a list of song_num
@return pages how many pages of songs will be printed.
    There's only 10 songs per page
@return song_list current 10 songs
"""
def showSongs(order):
    pages = int(len(order) / 10)
    song_ptr = 0
    for page in range(pages + 1):
        songs, song_ptr = getTenSongs(order, song_ptr)
        print("Page", str(page))    
        print("Title, Artist, Album, Length, Listen Count") 
        count = 0
        for song in songs.values(): 
            min, sec = divmod(song[3], 60000)
            time = "{:02d}:{:02d}".format(min, int(sec / 1000))
            print(str(count) + f": {song[0]}, {song[1]}, {song[2]}, {time}, {song[4]}") 
            count += 1
    return pages

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