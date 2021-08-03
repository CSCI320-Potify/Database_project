from src.cli import *
from src.account_access import *
from src.search import searchSong, searchUser
from src.Music_import import csv_import

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
        print("Your top 10 artists are - \n")
        while True:
            print("Select one of the 1 following options")
            print("1: Find songs - WARNING WILL LOOP")
            print("2: Find Users")
            print("3: Collections submenu")
            print("4: quit")
            choice = input()
            if choice == "1":
                searchSong()
            elif choice == "2":
                searchUser(current_user)
            elif choice == "3":
                collections(current_user)
            elif choice == "4":
                quit()
            else:
                print("Unknown command")
    else:
        main()
from src.Music_import import *

if __name__ == "__main__":
    main()