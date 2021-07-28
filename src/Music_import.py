from src.db import *
from collections import OrderedDict
import datetime
import csv


def csv_import(filename):
    csv = os.path.join(os.path.dirname(__file__), f'../{filename}')
    with open(csv, "r") as file:
        f = open("BAD NAMES", "w")
        next(file)
        song_num = 1
        artist_num = 1
        album_num = 1
        gen_id = 1

        connection = connect()
        cursor = connection.cursor()

        for line in file.readlines():

            list_of_genre =[]
            if(len(line.split("\"")) != 3):
                print(line + ": was skipped")
                f.write(line + "\n")
                continue
            try:
                temp_line = split(line)
            except:
                print(line + ": was skipped")
                f.write(line + "\n")
                continue
            temp_line_check = ""
            for i in temp_line[:-2]:
                temp_line_check+=","+i
            temp_line_check += ",\"" +temp_line[-2]+ "\","+temp_line[-1]
            temp_line_check = temp_line_check[1:]

            song, artist, album, duration, genre, year = [item for item in temp_line]
            if line != temp_line_check:
                print("mismatch " + line)
                print("temp " + temp_line_check + "\n")
                print("song: %s, artist: %s, album: %s, duration: %s, genre: %s, year: %s" % (song, artist, album, duration, genre, year))

            #Checks if song is currently logged
            cursor.execute('SELECT song_num FROM song WHERE "Title"=%s AND "length"=%s AND release_date=%s', (song, duration, year))
            duplicateSong = cursor.fetchone()

            if duplicateSong != None:
                print(line + "was duplicated")
                continue;


            #adds genres
            genre = genre[1:-1]
            genre.replace("'","")
            genrel = genre.split(",")
            for genre in genrel:
                score = ""
                for letter in genre:
                    if(genre!=" " and letter!="," and letter!="'"):
                        score+=letter
                cursor.execute('SELECT id FROM genre WHERE name=%s', [score])
                ge_id = cursor.fetchone()

                if ge_id == None:
                    ge_id = gen_id
                    gen_id += 1
                    cursor.execute('INSERT into genre(name, id) VALUES (%s, %s)', (score, ge_id))

                else:
                    #cursor.execute('SELECT "artist_num" FROM artist WHERE name=%s', ([artist]))
                    pass
                #adds for genre list
                list_of_genre.append(ge_id)

            #creates genre list
            cursor.execute('SELECT genre_list_id FROM genre_list')
            list_result = cursor.fetchall()

            list_id = len(list_result) + 1


            cursor.execute('INSERT INTO genre_list(genre_list_id) VALUES (%s)', [list_id])

            for genre in list_of_genre:
                cursor.execute('INSERT INTO "genre-genre_list"("genre_id", "genre_list_id") VALUES (%s, %s)',
                               (genre, list_id))

            #Adds song and song-genre
            cursor.execute('INSERT INTO Song("Title", release_date, "length", "song_num") VALUES (%s, %s, %s, %s)', (song, year, duration, song_num))
            cursor.execute('INSERT INTO "song-genre"("song_num", "genre_list") VALUES (%s, %s)',
                           (song_num, list_id))

            #artist
            cursor.execute('SELECT artist_num FROM artist WHERE name=%s', ([artist]))
            result = cursor.fetchone()

            if result == None:
                cursor.execute('INSERT into artist(name, "artist_num") VALUES (%s, %s)', (artist, artist_num))
                result = artist_num
            else:
                cursor.execute('SELECT artist_num FROM artist WHERE name=%s', ([artist]))
                result = cursor.fetchone()[0]
            #artist-song
            cursor.execute('INSERT INTO "artist-song"("artist_num", "song_num") VALUES (%s, %s)', (result, song_num))

            #album
            cursor.execute('SELECT album_num FROM album WHERE name=%s', ([album]))
            result_album_num = cursor.fetchone()

            if result_album_num == None:
                cursor.execute('INSERT into album(name, "album_num", duration, num_of_songs) VALUES (%s, %s, %s, %s)', (album, album_num, str(0), str(0)))
                result_album_num = album_num
            #else:
            #    result = len(cursor.fetchall()) + 1


            cursor.execute('SELECT MAX(track_num) FROM "song-album"')
            track_num = cursor.fetchone()[0] #what if their is no track num
            if track_num == None:
                track_num = 0

            #song album
            x = track_num+1

            cursor.execute('INSERT INTO "song-album"("album_num", "song_num", "track_num") VALUES (%s, %s, %s)', (result_album_num, song_num, x))

            cursor.execute('SELECT duration FROM album WHERE album_num=%s', ([result_album_num]))
            album_duration = cursor.fetchone()[0]
            cursor.execute('SELECT num_of_songs FROM album WHERE album_num=%s', ([result_album_num]))
            num_of_songs = cursor.fetchone()[0]
            cursor.execute('SELECT release_date FROM album WHERE album_num=%s', ([result_album_num]))
            release_date = cursor.fetchone()[0]
            cursor.execute('UPDATE album SET duration = %s WHERE album_num = %s', (album_duration + int(duration), result_album_num))
            cursor.execute('UPDATE album SET num_of_songs = %s WHERE album_num = %s',
                           (num_of_songs+1, result_album_num))
            new_year = max(int(release_date), int(year))
            cursor.execute('UPDATE album SET release_date = %s WHERE album_num = %s',
                           (new_year, result_album_num))

            #artist-album
            cursor.execute('SELECT album_num FROM "album-artist" WHERE artist_num=%s AND album_num=%s', (result, result_album_num))
            isThere = cursor.fetchone()


            if isThere == None:
                cursor.execute('INSERT into "album-artist"(artist_num, album_num) VALUES (%s, %s)', (result, result_album_num))

            #album genre_list
            cursor.execute('SELECT genre_list FROM "album-genre" WHERE album_num=%s', ([result_album_num]))
            a_glist = cursor.fetchone()

            if a_glist == None:
                list_id+=1;
                a_glist = list_id;
                cursor.execute('INSERT into "genre_list"(genre_list_id) VALUES (%s)', ([a_glist]))
                cursor.execute('INSERT into "album-genre"(album_num, genre_list) VALUES (%s,%s)', (result_album_num,a_glist))
            else:
                a_glist = a_glist[0]

            for genre in list_of_genre:
                cursor.execute('SELECT genre_list_id FROM "genre-genre_list" WHERE genre_list_id=%s AND genre_id=%s',(a_glist, genre))
                a_glist_there = cursor.fetchone()

                if a_glist_there == None:
                    cursor.execute('INSERT INTO "genre-genre_list"("genre_id", "genre_list_id") VALUES (%s, %s)',
                               (genre, a_glist))

            #artist genre
            cursor.execute('SELECT genre_list FROM "artist-genre" WHERE artist_num=%s', ([result]))
            ar_glist = cursor.fetchone()

            if ar_glist == None:
                list_id+=1;
                ar_glist = list_id;
                cursor.execute('INSERT into "genre_list"(genre_list_id) VALUES (%s)', ([ar_glist]))
                cursor.execute('INSERT into "artist-genre"(artist_num, genre_list) VALUES (%s,%s)', (result, ar_glist))
            else:
                ar_glist = ar_glist[0]

            for genre in list_of_genre:
                cursor.execute('SELECT genre_list_id FROM "genre-genre_list" WHERE genre_list_id=%s AND genre_id=%s',
                               (ar_glist, genre))
                ar_glist_there = cursor.fetchone()

                if ar_glist_there == None:
                    cursor.execute('INSERT INTO "genre-genre_list"("genre_id", "genre_list_id") VALUES (%s, %s)',
                                   (genre, ar_glist))



            song_num+=1
            album_num+=1
            artist_num+=1

        connection.commit()
        connection.close()
        file.close()
        f.close()

genres = []

def split2(line):
    global genres
    genres = []


    x = line.split("\\")
    assert(len(x) == 6)
    song = x[0]
    artist = x[1]
    album = x[2]
    duration = x[3]
    genre = x[4]
    year = x[5]


    gen = genre[1:-2]
    gen.replace(" ", ",")
    gen_arg = gen.split(",")
    for ge in gen_arg:
        if ge == " " or ge == "," or ge == "":
            continue
        genres += ge
    return song, artist, album, duration, genre, year



def split(line):


    if len(line.rsplit("\"",2)) == len(line):
        print("This line was change " + line + "\n")
        t_line = line
        t_line.replace("[", "]")
        x = t_line.split("]")
        rest = ""
        for i in x[:-2]:
            rest += i
        line = rest + "\"[" + x[-2] + "]\"" + x[-1]

    args = line.rsplit("\"",2)
    year = args[-1][1:]

    if(len(args) != 3):
        print("Line is " + line + "\n")
    genre = args[-2]
    args[-3] = args[-3][:-1]
    rest = args[-3].split(",")
    duration = rest[-1]
    artist = rest[-3]
    album = rest[-2]

    song = ""

    for word in rest[0:-4]:
        song += ", "+ word
    if(len(rest) == 4):
        song = rest[0]
    #bad apostrophe
    #song_el = song.split("'")
    #song = ""
    #for el in song_el:
    #    song += "'"+el
    #song  = song.split("'",1)[-1]




    #print("title: \"%s\", artist: %s, album: %s, duration: %s, genre: %s, year: %s\n" %(song, artist, album, duration, genre, year))


    genre_to_file(genre)
    return song, artist, album, duration, genre, year

def genre_to_file (genre):
    global genres
    genres = []
    gen = genre[1:-2]
    gen.replace(" ", ",")
    gen_arg = gen.split(",")
    for ge in gen_arg:
        if ge == " " or ge == "," or ge == "":
            continue
        genres += ge

#def split(line):
#    args = line.split(",", 4)
#    genre_year = args[-1].split(",")
#    args+= [genre_year[-1]]
#    args[-2] = genre_year[0:-1]
#    return args