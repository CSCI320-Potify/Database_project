import random

import pexpect
from src.cli import *

import winpexpect
from main import main as p
import names
import sys
import time

numerics = ["!","xxx", "FAZE", "crypto", "%","$","&","^","*"]
email_list = ["@yahoo", "@yandex", "@google", "@raytheon", "@rit", "@intel"]
dot_list = [".com", ".org", ".net", ".uk", ".phishing"]






def run():
    try:
        i = 0
        child = winpexpect.winspawn('cmd.exe', timeout=20)
        while True:
            main_menu = random.randint(1,2)
            time.sleep(5)



            child.logfile = sys.stdout
            child.expect('>', timeout=10000)
            child.sendline('cd C:\\Users\\raymo\\PycharmProjects\\Database_project') #The project directory

            time.sleep(1)
            #child.expect('3')
            child.sendline('python main.py')
            child.expect('3: Close client')

            connection = connect()
            cursor = connection.cursor()

            child.sendline(str(main_menu))
            if main_menu == 1: #login
                cursor.execute('SELECT username, password from "user" ORDER BY random()')
                [user_name, password] = cursor.fetchone()
                child.expect("Enter username:")
                child.sendline(user_name)
                child.expect("Enter password:")
                child.sendline(password)
                print(user_name)
                cursor.execute('SELECT email from "user" where username = %s', ([user_name]))
                email = cursor.fetchone()[0]

            else: #create account
                first_name = names.get_first_name()
                last_name = names.get_last_name()
                user_name = numerics[random.randint(0,len(numerics)-1)] + first_name + last_name + str(random.randint(0,10000)) + numerics[random.randint(0,len(numerics)-1)]
                password = str(random.randint(0,10000000)) + names.get_full_name()
                email = first_name + last_name + str(random.randint(0,10000)) + numerics[random.randint(0,len(numerics)-1)] + email_list[random.randint(0,len(email_list)-1)] + dot_list[random.randint(0,len(dot_list)-1)]
                child.expect("Enter First Name:")
                child.sendline(first_name)
                child.expect("Enter Last Name:")
                child.sendline(last_name)
                child.expect("Enter Username:")
                child.sendline(user_name)
                child.expect("Enter Password:")
                child.sendline(password)
                child.expect("Enter Email:")
                child.sendline(email)


            child.expect("quit")
            sub_menu = random.randint(2,3) ######################might be 2,3
            child.sendline(str(sub_menu))

            if sub_menu == 2: #find users
                cursor.execute('Select email from "user" ORDER BY random()')
                friend_email_index = 1;
                tot_friend_email = cursor.fetchall()
                friend_email = tot_friend_email[0]
                while friend_email == email:
                    friend_email = tot_friend_email[friend_email_index]
                    friend_email_index +=1
                    friend_email_index %= len(tot_friend_email)
                child.expect("Enter email of user to search for:")
                print("friend_email is " + friend_email[0])
                child.sendline(friend_email[0])
                possiblity = child.expect(["Email has user" , "User Not Found", "Returning to options select"])
                if possiblity == 0:
                    child.expect("You are not currently following this user, would you like to follow?")
                    child.sendline(str(random.randint(1, 2)))
                elif possiblity == 1:
                    child.expect("You are already following this user, would you like to unfollow?")
                    child.sendline(str(random.randint(1, 2)))
            if sub_menu == 3: #collections
                child.expect("Select one of the following options")
                collections_options = ["1", "2", "5"][random.randint(0, 2)]
                cursor.execute('SELECT name from collection where username = %s', ([user_name]))
                collection_list = cursor.fetchall()
                if (len(collection_list) == 0):
                    collections_options = "2"

                child.sendline(collections_options)

                if(collections_options == "1"): #add to collection
                    child.expect("What is the name of the collection you wish to add to?")
                    child.sendline(collection_list[random.randint(0,len(collection_list)-1)])
                    child.expect("What is the name of the song you wish to add to") #regex
                    cursor.execute('SELECT "Title" from song order by random()')
                    child.sendline(cursor.fetchone[0])
                    while(random.randint(0,2) != 2):
                        adding_poss = child.expect(["What is the name of the collection you wish to add to?", "This song is already in the collection."])
                        if adding_poss == 1:
                            child.sendline(collection_list[random.randint(0,len(collection_list)-1)])
                            child.expect("What is the name of the song you wish to add to")  # regex
                            cursor.execute('SELECT "Title" from song order by random()')
                            child.sendline(cursor.fetchone[0])
                        else:
                            continue
                    child.expect(["What is the name of the collection you wish to add to?",
                                   "This song is already in the collection.",
                                   "What is the name of the song you wish to add to Song?"])
                    child.sendline("quit")

                elif(collections_options == "2"): #create new collection
                    child.expect("What is the name of the collection you wish to add?")
                    collection_name = ["Party Mix ", "Disco ", "Epic ", "Too Groovy ", "Bass Boosted ", ""][random.randint(0,5)]+ names.get_full_name() +" "+numerics[random.randint(0,len(numerics)-1)]
                    if(len(collection_name)>=19):
                        collection_name = collection_name[0:17]
                    child.sendline(collection_name)
                else: #play collection
                    child.expect("What is the name of the collection you wish to play?")
                    child.sendline(collection_list[random.randint(0,len(collection_list)-1)])
                child.expect("Select one of the following options")
                child.sendline("8")

            child.expect("5: quit")
            cursor.close()
            child.sendline(str(5))

            print(str(i) +"th time access successful")
            i += 1
    except Exception as e:
        if not isinstance(e, pexpect.TIMEOUT):
            print(e)
        child.close()
        run()
try:
    run()
except:
    run()