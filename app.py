from colorama import Fore, Style
from getpass import getpass
from service.user_service import UserService
from service.news_service import NewsService

from time import sleep

import enum
import os
import sys


class Menu(enum.IntEnum):
    LOGIN = 1
    LOGOUT = 9
    EXIT = 0
    RETURN = 0

    NEWS_MANAGEMENT = 1
    USER_MANAGEMENT = 2

    AUDIT_NEWS = 1
    DELETE_NEWS = 2


class State(enum.Enum):
    DRAFT = "draft"
    APPROVED = "approved"
    PENDING = "pending"
    HIDDEN = "hidden"


def display_welcome():
    """
    display welcome message
    """
    os.system("cls")
    print(Fore.LIGHTBLUE_EX, "\n\t" + "=" * 50)
    print(Fore.LIGHTBLUE_EX, "\n\tWelcome to the News Management System")
    print(Fore.LIGHTBLUE_EX, "\n\t" + "=" * 50)
    print(Fore.LIGHTGREEN_EX, "\n\t{}. {}".format(Menu.LOGIN, Menu.LOGIN.name.title()))
    print(Fore.LIGHTGREEN_EX, "\n\t{}. {}".format(Menu.EXIT, Menu.EXIT.name.title()))
    print(Style.RESET_ALL)


def display_invalid_input_message(second=1):
    """
    output the message with the countdown time
    :param second: countdown time
    """
    for i in range(second * -1, 1):
        if i == 0:
            print(Fore.RED, "\r\tInvalid input!")
        else:
            print(Fore.RED, "\r\tInvalid input!(return in {}S)".format(i * -1), end="")
            sleep(1)


def display_admin_menu():
    os.system("cls")
    print(Fore.LIGHTGREEN_EX, "\n\t{}. News management".format(Menu.NEWS_MANAGEMENT))
    print(Fore.LIGHTGREEN_EX, "\n\t{}. User management".format(Menu.USER_MANAGEMENT))
    print(Fore.LIGHTRED_EX, "\n\t{}. Logout".format(Menu.LOGOUT))
    print(Fore.LIGHTRED_EX, "\n\t{}. Exit".format(Menu.EXIT))
    print(Style.RESET_ALL)


def display_news_management_menu():
    os.system("cls")
    print(Fore.LIGHTGREEN_EX, "\n\t{}. Audit news".format(Menu.AUDIT_NEWS))
    print(Fore.LIGHTGREEN_EX, "\n\t{}. Delete news".format(Menu.DELETE_NEWS))
    print(Fore.LIGHTRED_EX, "\n\t{}. Return".format(Menu.RETURN))
    print(Style.RESET_ALL)


while True:

    display_welcome()

    # get the user choose
    opt = input("\n\tPlease input operation num: ")
    if opt == str(Menu.LOGIN.value):
        username = input("\n\tUsername: ")
        # password = getpass("\n\tPassword: ")
        password = input("Password: ")

        # login result
        login_result = UserService.login(username, password)

        # login successful
        if login_result == True:
            # get user's role
            user_role = UserService.search_user_role(username)
            # display admin menu
            if user_role == "admin":
                while True:
                    display_admin_menu()
                    opt = input("\n\tPlease input: ")
                    if opt == str(Menu.NEWS_MANAGEMENT.value):
                        while True:
                            display_news_management_menu()
                            opt = input("\n\tPlease input: ")

                            # display all pending news
                            if opt == str(Menu.AUDIT_NEWS.value):
                                news_state = State.PENDING.value
                                print(news_state)
                                page = 1
                                while True:
                                    result = NewsService.get_newslist_by_state_page(news_state, page)
                                    total_page = NewsService.get_news_total_page_by_state(news_state)
                                    if result is not None:
                                        for index in range(len(result)):
                                            news = result[index]
                                            print(Fore.LIGHTBLUE_EX,
                                                  "\n\t{idx}. {title} {editor} {create_time}".format(idx=index + 1,
                                                                                                     title=news[1],
                                                                                                     editor=news[2],
                                                                                                     create_time=news[
                                                                                                         3]))
                                        print(Fore.CYAN, "\n\t" + "-" * 10)
                                        print(Fore.CYAN, "\n\t{}/{}".format(page, total_page))
                                        print(Fore.CYAN, "\n\t" + "-" * 10)
                                        print(Fore.LIGHTCYAN_EX, "\n\tback. Prev page")
                                        print(Fore.LIGHTCYAN_EX, "\n\tnext. Next page")
                                        print(Fore.LIGHTRED_EX, "\n\t{}. Return".format(Menu.RETURN))
                                        print(Style.RESET_ALL)
                                        # audit news
                                        opt = input("\n\tPlease input: ")
                                        if opt == str(Menu.RETURN.value):
                                            break
                                        elif opt.lower() == "back" and page > 1:
                                            page -= 1
                                        elif opt.lower() == "next" and page < total_page:
                                            page += 1
                                        elif opt.isdigit():
                                            change_state = State.APPROVED.value
                                            news_id = result[int(opt) -1][0] #get id
                                            NewsService.update_news_state(news_id, change_state)
                                            # pass
                                        else:
                                            print(display_invalid_input_message())

                                    else:
                                        print(Fore.RED, "\n\tNo news in pending")

                            elif opt == str(Menu.DELETE_NEWS.value):
                                pass
                            elif opt == str(Menu.RETURN.value):
                                break
                            else:
                                display_invalid_input_message(3)
                    elif opt == str(Menu.USER_MANAGEMENT.value):
                        pass
                    elif opt == str(Menu.LOGOUT.value):
                        break
                    elif opt == str(Menu.EXIT.value):
                        sys.exit()
                    else:
                        display_invalid_input_message(5)


            # display editor menu
            elif user_role == "editor":
                print(username + "---" + user_role)
                sleep(2)

        # login failed
        else:
            print(Fore.RED, "Username or Password not correct! Please check it and login again!")
            sleep(2)

    # exit the system
    elif opt == str(Menu.EXIT.value):
        sys.exit()
    else:
        display_invalid_input_message(3)
