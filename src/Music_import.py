from src.db import *
import csv


def csv_import(filename):
    csv = os.path.join(os.path.dirname(__file__), f'../{filename}')
    with open(csv, "r") as file:
        next(file)
        song_num = 7
        artist_num = 1
        album_num = 1
        #for line in csv.reader(file, delimiter=","):
        for line in file.readlines():
            connection = connect()
            cursor = connection.cursor()
            temp_line = split(line)
            song, artist, album, duration, genre, year = [item for item in temp_line]
            connection = connect()
            cursor = connection.cursor()
            print(song_num)
            cursor.execute('INSERT INTO Song("Title", release_date, "length", "song_num") VALUES (%s, %s, %s, %s)', (song, year, duration, song_num))

            #artist
            cursor.execute('SELECT "artist_num" FROM artist WHERE name=%s', ([artist]))
            result = cursor.fetchone()

            if result == None:
                cursor.execute('INSERT into artist(name, "artist_num") VALUES (%s, %s)', (artist, artist_num))
                result = artist_num
            else:
                cursor.execute('SELECT "artist_num" FROM artist WHERE name=%s', ([artist]))
                result = cursor.fetchone()[0]
            #artist-song
            cursor.execute('INSERT INTO "artist-song"("artist_num", "song_num") VALUES (%s, %s)', (result, song_num))

            #album
            cursor.execute('SELECT "album_num" FROM album WHERE name=%s', ([album]))
            result_album_num = cursor.fetchone()

            if result_album_num == None:
                cursor.execute('INSERT into album(name, "album_num", duration) VALUES (%s, %s, %s)', (album, album_num, duration))
                result_album_num = album_num
            else:
                result = cursor.fetchone()[0]


            cursor.execute('SELECT MAX("track_num") FROM "song-album"')
            track_num = cursor.fetchone()[0] #what if their is no track num
            if track_num == None:
                track_num = 0

            #song album
            x = track_num+1
            cursor.execute('INSERT INTO "song-album"("album_num", "song_num", "track_num") VALUES (%s, %s, %s)', (result_album_num, song_num, x))

            cursor.execute('SELECT duration FROM album WHERE album_num=%s', ([result_album_num]))
            album_duration = cursor.fetchone()[0]
            cursor.execute('UPDATE album SET duration = %s WHERE album_num = %s', (album_duration + int (duration), result_album_num))

            #artist-album
            cursor.execute('SELECT COUNT(*) FROM "album-artist" WHERE artist_num=%s AND album_num=%s', (result, result_album_num))
            isThere = cursor.fetchone()[0]

            if isThere == 0:
                cursor.execute('INSERT into "album-artist"(artist_num, album_num) VALUES (%s, %s)', (result, result_album_num))

            song_num+=1
            album_num+=1
            artist_num+=1

def split(line):
    args = line.split(",", 4)
    genre_year = args[-1].split(",")
    args+= [genre_year[-1]]
    args[-2] = genre_year[0:-1]
    return args
