import math
import os
import pickle
import sys
import time
import datetime
import pandas
import getpass

distillation_dict = {}
# ### FUNCTIONS ###


def load_data():
    # Looks for login data files.
    try:
        file_object = open('logins.pydata', 'rb')
        data = pickle.load(file_object)
        file_object.close()
        return data
    # If file not found, creates temporary list to store login.
    except Exception as e:
        print(e)
        print("No database. Creating list.")
        return []


def save_data():
    # Saves login data file
    try:
        file_object = open('logins.pydata', 'wb')
        pickle.dump(logins, file_object)
        file_object.close()
    except Exception as e:
        print("Not able to save data.")
        print(e)


def on_start():
    # Looks for dictionary data file
    try:
        file_object = open('dicts/lists.pydata', 'rb')
        my_dictionary = pickle.load(file_object)
        file_object.close()
        return my_dictionary
    except Exception as e:
        print(e)
        print("NO DICTIONARY PRESENT YET")
        return {}


def dict_load():
    # Loads in CSV dictionary file
    df_dictionary = pandas.read_csv('dictionary.csv')
    df_dictionary.columns = ['word', 'grammar', 'explanation']
    df_word_explanation = df_dictionary[['word', 'explanation']]
    return df_word_explanation


def save_dict():

    current_dir = os.getcwd()

    dict_dir = os.path.join(current_dir, r'dicts')
    if not os.path.exists(dict_dir):
        os.makedirs(dict_dir)

    os.chdir(dict_dir)

    try:
        file_object = open('lists.pydata', 'wb')
        pickle.dump(dictionary, file_object)
        file_object.close()
        print("Data Created.")
    except Exception as e:
        print("UNABLE TO SAVE DICTIONARY FILE.")
        print(e)


def login():
    # Handles user login
    logo()

    username = input("\n\t\tUSERNAME: ")
    print()
    if username == "q":
        print("\n\tPROGRAM TERMINATES")
        save_dict()
        time.sleep(0.5)
        sys.exit()
    password = getpass.getpass("\t\tPASSWORD: ")  # makes user password invisible
    if username and password not in logins:
        print("\nUSERNAME OR PASSWORD INCORRECT")
        time.sleep(1)
        account = input("\nCREATE ACCOUNT? (y/n)")
        if account == ("Y", "y", "YES", "yes"):
            print("\nACCOUNT CREATED")
            for n in range(3):
                print("•", end=' ')
                time.sleep(0.5)
            logins.append(username)
            logins.append(password)
            save_data()
            interface()
        else:
            time.sleep(1)
            os.system('clear')
            login()
    else:
        time.sleep(1)
        show_menu()
    return username


def pages_count():
    pgs = (len(dictionary) / 25) + 1
    pgs = math.floor(pgs)
    if pgs == 0:
        pgs = 1
    return pgs


def words_count():
    wds = len(dictionary)
    if wds <= 25:
        wds = len(dictionary)
    elif wds > 25:
        wds = len(dictionary) - (25 * (pages_count() - 1))
    else:
        print("FAILED TO FIND PAGE NO")
    return wds


def show_dict():
    print("\nCURRENT DICTIONARY PAGE: {} \n".format(pages_count()))
    print(dictionary)
    # n = 1
    # for x in list(dictionary)[-words_count():]:
    #     print("{}. {}".format(n, x))
    #     n += 1
    #     time.sleep(0.2)
    input("")


def show_pages():
    print("THERE ARE {} PAGES IN YOUR DICTIONARY".format(pages_count()))
    page_no = input("CHOSE PAGE: ")
    try:
        n = 1
        if int(page_no) == 1:
            for k in list(dictionary)[:25]:
                print(n, k)
                n += 1
            user_input()
        elif int(page_no) > 1:
            for k in list(dictionary)[(int(page_no) * 25) - 25:((int(page_no) * 25) - 25) + 25]:
                print(n, k)
                n += 1
            user_input()
    except ValueError:
        print("Invalid Input")


def interface():
    # Main application interface

    # loads in one word - explanation pair from dictionary CSV file
    sample = word_explanation.sample(1)
    final_word = sample.to_string(index=False, header=False)
    word = str(final_word.split(' ')[1])
    explanation = ' '.join(final_word.split(' ')[3:])
    explanation = str(explanation)

    os.system('clear')

    if len(dictionary) == 5:
        save_dict()

    wds = len(dictionary)
    if wds <= 25:
        wds = len(dictionary)
    elif wds > 25:
        wds = len(dictionary) - (25 * (pages_count()-1))
    else:
        print("FAILED TO FIND PAGE NO")

    print("*** 🅆🄾🅁🄳 ********** 🄴🅇🄿🄻🄰🄽🄰🅃🄸🄾🄽  *** WORDS ON PAGE {} * PAGE NO {}\n".format(wds, pages_count()))
    print("***", str(word) + ' ', end='')
    for x in range(22 - len(word) - 4):
        print("*", end='')
    print(' ' + str(explanation), '\n')

    user_input()


def combine_lists(data, n):
    dictionary[n] = data
    return dictionary


def user_input():

    user_word = input()
    if user_word == "":
        interface()
    elif user_word == "s":
        n = input("Name list: ")
        combine_lists(new_list, n)
        show_menu()
    elif user_word == "q":
        login()
    else:
        try:
            word = user_word.split(' ', 1)[0]
            explanation = user_word.split(' ', 1)[1]
            word = word.title()
            explanation = explanation.title()
            new_list[word] = explanation
            interface()
        except IndexError:
            print("\n\tEXPLANATION MUST NOT BE BLANK.")
            time.sleep(2)
            interface()


def distillation():

    print("WHICH PAGE WOULD YOU LIKE TO DISTILL")
    page_no = input("CHOSE PAGE: ")

    try:
        n = 1
        if int(page_no) == 1:
            for k in list(dictionary):
                print(n, k, end=' - ')
                user_word = input()
                if user_word == "q":
                    interface()
                if len(user_word) > 0:
                    distillation_dict[k] = user_word.title()
                else:
                    continue
        elif int(page_no) > 1:
            for k in list(dictionary)[(int(page_no) * 25) - 25:((int(page_no) * 25) - 25) + 25]:
                print(n, k)
                n += 1
            user_input()
    except ValueError:
        print("Invalid Input")


def show_distill():
    print("YOUR DISTILLED WORDS: ")
    print(distillation_dict)


def introduction():
    print()
    print("\tStruggling with learning a foreign language? ")
    time.sleep(1)
    print("\tTired of flashcards and memorising glossaries? ")
    time.sleep(1)
    print("\tIf so, the GOLD LIST method may help.")

    input()
    os.system('clear')

    print()
    print(" +-------------------------+ +--------------------------+")
    print(" |                         | |                          |")
    print(" |                         --->                         |")
    print(" |                         | |                          |")
    print(" |                         | |      1st DISTILLATION    |")
    print(" |        MAIN LIST        | |          17 WORDS        |")
    print(" |        25 WORDS         | |                          |")
    print(" |                         | |                          |")
    print(" |                         | |                          |")
    print(" |   ▲                     | +----------------------|---+")
    print(" +---|---------------------+ +----------------------|---+")
    print(" +---|---------------------+ |                      ▼   |")
    print(" |                         | |                          |")
    print(" |                         | |      2nd DISTILLATION    |")
    print(" |    3rd DISTILLATION     | |          11 WORDS        |")
    print(" |        7 WORDS         <---                          |")
    print(" |                         | |                          |")
    print(" |                         | |                          |")
    print(" +-------------------------+ +--------------------------+")
    print()
    print("\tYou start by typing words from the dictionary.")
    time.sleep(1)
    print("\tThen you wait for at least two weeks to find out")
    time.sleep(1)
    print("\tthat you almost miraculously remembered 30% words")
    time.sleep(1)
    print("\tfrom each list. All thanks to the power of moving information")
    time.sleep(1)
    print("\tfrom short to long-term memory")
    input()
    os.system('clear')


def logo():
    print()
    print("\n  ░██████╗░░█████╗░██╗░░░░░██████╗░  ██╗░░░░░██╗░██████╗████████╗")
    print("  ██╔════╝░██╔══██╗██║░░░░░██╔══██╗  ██║░░░░░██║██╔════╝╚══██╔══╝")
    print("  ██║░░██╗░██║░░██║██║░░░░░██║░░██║  ██║░░░░░██║╚█████╗░░░░██║░░░")
    print("  ██║░░╚██╗██║░░██║██║░░░░░██║░░██║  ██║░░░░░██║░╚═══██╗░░░██║░░░")
    print("  ╚██████╔╝╚█████╔╝███████╗██████╔╝  ███████╗██║██████╔╝░░░██║░░░")
    print("  ░╚═════╝░░╚════╝░╚══════╝╚═════╝░  ╚══════╝╚═╝╚═════╝░░░░╚═╝░░░")
    print("  𝕓𝕪 ℝ𝕒𝕕𝕖𝕜                                  PRESS q to QUIT\n")
    print()


def show_menu():

    logo()
    print()
    print("\t1. YOUR DICTIONARY")
    print("\t2. YOUR PAGES")
    print("\t3. YOUR DISTILLATIONS")
    print("\t4. YOUR ACCOUNT")
    print("\n\t PRESS 'S' TO START ")
    print()
    print()

    option_input = input()
    if str(option_input).lower() == "s":
        interface()
    if int(option_input) == 1:
        show_dict()
        input()
        show_menu()
    elif int(option_input) == 2:
        show_pages()
        input()
        show_menu()
    elif int(option_input) == 3:
        show_distill()
        input()
        show_menu()
    elif int(option_input) == 4:
        show_account()
        input()
        show_menu()
    elif str(option_input).lower() == "s":
        interface()
    else:
        print("\nINVALID INPUT")
        time.sleep(1)
        show_menu()
    os.system('clear')


def show_account():

    logo()
    print()
    print("\tSOME OPTIONS: ")
    print()
    print("\n\t PRESS 'S' TO START ")
    interface()
    print("\n\t PRESS 'Q' TO START ")
    option_input = input()
    if option_input.lower() == "s":
        interface()
    elif option_input.lower() == "q":
        show_menu()
    else:
        print("\nINVALID INPUT")
        time.sleep(1)
        show_account()


new_list = {}
word_explanation = dict_load()
dictionary = on_start()
logins = load_data()
# introduction()
login()

