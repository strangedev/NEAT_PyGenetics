from Testing.Tools.NEATCommander.TermIO import *
from Testing.Tools.NEATCommander.SessionRunner import *

def __main__():
    print("(>^.^)> NEATCommander!\n\n")
    response = ""
    while response != "exit":
        response = display_main_menu()
        if response == "start":
            run_session()

def display_main_menu():
    print_headline("Choose an action")
    display_choice(
        [
            "Start a session",
            "Exit"
        ]
    )
    choice = int(get_input())
    if choice == 1:
        return "start"
    elif choice == 2:
        return "exit"

__main__()