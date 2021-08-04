from src.cli import *
from src.account_access import *
from src.search import searchSong, searchUser
from src.Music_import import csv_import


def top_artists(user):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM "user-song" WHERE username=%s', [user])
    played_songs = cursor.fetchone()[0]
    if played_songs == 0:
        print("You do not have any favorite artists yet. Go and play some music!")
    elif played_songs == 1:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s OFFSET 0', [user])
        song_num = cursor.fetchone()[0]
        cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_num])
        artist_num = cursor.fetchone()[0]
        cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_num])
        artist = cursor.fetchone()[0]
        print("Your top artist is", artist + ".")
    elif played_songs == 2:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 2 ROWS ONLY', [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1"]
        artist = ["0", "1"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0], "and", artist[1] + ".")
    elif played_songs == 3:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 3 ROWS ONLY', [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2"]
        artist = ["0", "1", "2"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1], "and", artist[2] + ".")
    elif played_songs == 4:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 4 ROWS ONLY', [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3"]
        artist = ["0", "1", "2", "3"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2], "and", artist[3] + ".")
    elif played_songs == 5:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 5 ROWS ONLY', [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3", "4"]
        artist = ["0", "1", "2", "3", "4"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2] + ",", artist[3], "and", artist[4] + ".")
    elif played_songs == 6:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 6 ROWS ONLY',
                       [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3", "4", "5"]
        artist = ["0", "1", "2", "3", "4", "5"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2] + ",", artist[3] + ",", artist[4], "and", artist[5] + ".")
    elif played_songs == 7:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 7 ROWS ONLY',
                       [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3", "4", "5", "6"]
        artist = ["0", "1", "2", "3", "4", "5", "6"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2] + ",", artist[3] + ",", artist[4] + ",", artist[5], "and", artist[6] + ".")
    elif played_songs == 8:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 8 ROWS ONLY',
                       [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3", "4", "5", "6", "7"]
        artist = ["0", "1", "2", "3", "4", "5", "6", "7"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2] + ",", artist[3] + ",", artist[4] + ",", artist[5] + ",", artist[6], "and", artist[7] + ".")
    elif played_songs == 9:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 9 ROWS ONLY',
                       [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        artist = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2] + ",", artist[3] + ",", artist[4] + ",", artist[5] + ",", artist[6] + ",", artist[7], "and", artist[8] + ".")
    else:
        cursor.execute('SELECT song_num FROM "user-song" WHERE username=%s ORDER BY play_count DESC FETCH NEXT 10 ROWS ONLY',
                       [user])
        song_nums = cursor.fetchall()
        artist_nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        artist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for i in range(len(song_nums)):
            cursor.execute('SELECT artist_num FROM "artist-song" WHERE song_num=%s', [song_nums[i][0]])
            artist_nums[i] = cursor.fetchone()[0]
        for i in range(len(artist_nums)):
            cursor.execute('SELECT name FROM "artist" WHERE artist_num=%s', [artist_nums[i]])
            artist[i] = cursor.fetchone()[0]
        print("Your top artists are", artist[0] + ",", artist[1] + ",", artist[2] + ",", artist[3] + ",", artist[4] + ",",
              artist[5] + ",", artist[6] + ",", artist[7] + ",", artist[8] + "and", artist[9] + ".")


def main():
    # csv_import("top1000_songs.csv")
    populateTestData()
    current_user = ''
    print("Welcome to Potify")
    print("Select one of the following options")
    print("1: Login to account")
    print("2: Create new account")
    print("3: Close client")
    choice = input()

    if choice == "1":
        current_user = login()
    elif choice == "2":
        current_user = signup().strip()
    elif choice == "3":
        quit()
    else:
        print("Unknown command")
        quit()

    if current_user != '':
        print("Welcome Back " + current_user)
        connection = connect()
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) from "collection" WHERE username=%s', [current_user])
        collect_amt = cursor.fetchone()[0]
        print("You have", collect_amt, "collections.")
        cursor.execute('SELECT COUNT(*) from "friends" WHERE follows=%s', [current_user])
        followers = cursor.fetchone()[0]
        print("You have", followers, "followers.")
        cursor.execute('SELECT COUNT(*) from "friends" WHERE "user"=%s', [current_user])
        following = cursor.fetchone()[0]
        if following == 1:
            print("You are following 1 person.")
        else:
            print("You are following", following, "people.")
        top_artists(current_user)
        while True:
            print("Select one of the 1 following options")
            print("1: Find songs - WARNING WILL LOOP")
            print("2: Find Users")
            print("3: Collections submenu")
            print("4: Recommendations")
            print("5: quit")
            choice = input()
            if choice == "1":
                searchSong()
            elif choice == "2":
                searchUser(current_user)
            elif choice == "3":
                collections(current_user)
            elif choice == "4":
                Recommendation(current_user)
            elif choice == "5":
                quit()
            else:
                print("Unknown command")
            connection.close()
    else:
        main()
from src.Music_import import *

if __name__ == "__main__":
    main()