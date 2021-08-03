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
    else:
        main()
from src.Music_import import *

if __name__ == "__main__":
    main()