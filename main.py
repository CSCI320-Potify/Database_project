from src.cli import *


def main():
    user = ''
    print("Welcome to Potify")
    print("Select one of the following options")
    print("1: Login to account")
    print("2: Create new account")
    print("3: Close cli")
    print("4: show all tables")
    choice = int(input())

    if choice == 1:
        user = login()
    elif choice == 2:
        user = signup()
    elif choice == 3:
        quit()
    elif choice == 4:
        show()
    else:
        print("Incorrect choice")
        quit()

    if user != '':
        while True:
            print("Hello" + user)
            print("Select one of the following options")
            print("1: Collections submenu")
            print("2: Find songs")
            print("3: Find Users")
    


main()