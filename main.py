from src.cli import *


def main():
    populateTestData()
    current_user = ''
    print("Welcome to Potify")
    print("Select one of the following options")
    print("1: Login to account")
    print("2: Create new account")
    print("3: Close cli")
    choice = int(input())

    if choice == 1:
        current_user = login()
    elif choice == 2:
        current_user = signup()
    elif choice == 3:
        quit()
    else:
        print("Incorrect choice")
        quit()

    if current_user != '':
        print("Welcome Back " + current_user)
        while True:
            print("Select one of the following options")
            print("1: Find songs")
            print("2: Find Users")
            print("3: Collections submenu")
            print("4: quit")
            choice = int(input())
            if choice == 1:
                songSearch()
            elif choice == 2:
                searchUser(current_user)
            elif choice == 3:
                print("temp")
            elif choice == 4:
                quit()
            else:
                print("Incorrect choice")
                quit()


main()