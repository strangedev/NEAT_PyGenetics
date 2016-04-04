from NEAT.Networking.Commands.CommandTranscoder import CommandTranscoder
from NEAT.Networking.Server.JSONSocket import JSONSocket


class NEATClient(object):

    def __init__(self, server_address, server_port):
        self._server_address = server_address
        self._server_port = server_port

    def _send_command(self, command):
        socket = JSONSocket(
            self._server_address,
            self._server_port
        )
        try:
            socket.send_dict(
                CommandTranscoder.encode_command(
                    command
                )
            )
        except Exception:
            return False
        return True

    def _receive_result(self):
        socket = JSONSocket(
            self._server_address,
            self._server_port + 1
        )
        try:
            print("Trying to receive dict...")
            dictionary = socket.receive_dict()
        except Exception as e:
            print(e)
            return None

        if "_type" in dictionary.keys():
            if dictionary["_type"] in CommandTranscoder.type_class_map.keys():
                response = CommandTranscoder.decode_command(dictionary)
                return response
        return dictionary

    def run_command(self, command):
        message_sent = self._send_command(command)
        if message_sent:
            print("Message has been sent.")
            return self._receive_result()
        return None
