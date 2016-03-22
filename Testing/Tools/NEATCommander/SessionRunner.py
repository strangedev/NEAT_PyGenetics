from Testing.Tools.NEATCommander.TermIO import *
from Testing.Tools.NEATCommander.Commander import *

def run_session():
    print_headline("Start a new session")
    print("To start a new session, you have to provide")
    print("a session id. This id will uniquely identify")
    print("your session.")
    print("A session contains all of your genomes, as")
    print("well as their fitness values, all of the")
    print("genomes that were once alive during your")
    print("simulation runs, meaning all of your data")
    print("is stored within it - to create a new session")
    print("you will have to pick a previously unused")
    print("session id.")
    print("")
    session_id = "neat little session"
    block_size = 1
    config_path = "../../../NEAT/Config/"
    while True:
        print_headline("Session configuration")
        display_choice(
            [
                "Session Id: " + session_id,
                "Block Size: " + str(block_size),
                "Path to configuration files: " + config_path,
                "Start the session"
            ]
        )
        edit_index = int(
            get_input(
                message="Choose an entry to edit, or start"
            )
        )
        if edit_index == 4:
            start_commanding(
                session_id,
                block_size,
                config_path
            )
        elif edit_index == 1:
            session_id = edit_string(session_id)
        elif edit_index == 2:
            block_size = int(edit_string(str(block_size)))
        elif edit_index == 3:
            config_path = edit_string(config_path)






