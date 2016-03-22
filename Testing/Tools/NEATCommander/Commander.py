from Testing.Tools.NEATCommander.TermIO import *
from NEAT.Networking.Client.SimulationClient import SimulationClient
from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException

def start_commanding(session_id, block_size, config_path):

    print_headline("Connect to a server")
    print("You will have to connect to a NEAT Server.")
    server_address = "127.0.0.1"
    server_port = 8081
    display_choice(
        [
            "IP Address: " + server_address,
            "Port: " + str(server_port),
            "Connect"
        ]
    )
    edit_index = int(
        get_input(
            "Choose an entry to edit"
        )
    )
    if edit_index == 1:
        server_address = edit_string(server_address)
    elif edit_index == 2:
        server_port = int(edit_string(str(server_port)))
    elif edit_index == 3:
        client = SimulationClient(server_address, server_port)

        try:
            client.announce_session(
                session_id,
                config_path,
                block_size
            )
        except NetworkProtocolException as e:
            print(e)
            return

