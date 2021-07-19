from src.cli import *
from src.account_access import *
from src.search import searchSong, searchUser

def main():
    #csv_import("top1000_songs.csv")
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
            print("1: Find songs")
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


if __name__ == "__main__":
    main()