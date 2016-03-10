from NEAT.Networking.Server.JSONSocket import JSONSocket
from NEAT.Networking.Commands.CommandTranscoder import CommandTranscoder

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

    def _recv_result(self):
        socket = JSONSocket(
            self._server_address,
            self._server_port
        )
        try:
            dictionary = socket.receive_dict()
        except Exception:
            return None
        return CommandTranscoder.decode_command(dictionary)

    def run_command(self, command):
        message_sent = self._send_command(command)
        if message_sent:
            return self._recv_result()
        return None