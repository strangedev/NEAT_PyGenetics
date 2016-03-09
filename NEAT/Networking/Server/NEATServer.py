import socket
import json
from threading import Thread

class JSONSocket(Thread):

    def __init__(
        self,
        server_address,
        server_port
    ):
        super().__init__()

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self._server_address = server_address
        self._server_port = server_port
        self._connection_alive = True

    @property
    def connection_alive(self):
        return self._connection_alive

    def close_connection(self):
        if self.connection_alive:
            self._socket.close()
            self._connection_alive = False

    def _receive_message(self, socket):

        message_size = self._receive_message_size(socket)

        message_chunks = []
        bytes_received = 0

        while bytes_received < message_size:
            chunk = self._socket.recv(
                min(
                    message_size - bytes_received,
                    1024
                )
            )
            if chunk == "":
                raise RuntimeError("JSONSocket: socket broken")
            message_chunks.append(chunk)
            bytes_received += len(chunk)

        return ''.join(message_chunks)

    def _receive_message_size(self, socket):

        message_size_serialized = ""
        bytes_sent = 0

        while bytes_sent < 16:
            chunk = self._socket.recv(
                min(
                    16 - bytes_sent,
                    16
                )
            )
            if chunk == '':
                raise RuntimeError("JSONSocket: socket broken")
            message_size_serialized += chunk
            bytes_sent += len(chunk)

        return int(message_size_serialized)

    def _send_message(self, message: str):

        message_size = len(message)
        bytes_sent = 0

        message_size_serialized  = self._serialize_message_size(message_size)

        while bytes_sent < 16:
            sent = self._socket.send(
                message_size_serialized
            )
            if sent == 0:
                raise RuntimeError("JSONSocket: socket broken")
            bytes_sent += sent

        bytes_sent = 0
        while bytes_sent < message_size:
            sent = self._socket.send(
                message[bytes_sent:]
            )
            if sent == 0:
                raise RuntimeError("JSONSocket: socket broken")
            bytes_sent += sent

    def _serialize_message_size(self, message_size):
        as_string = str(message_size)
        length = len(as_string)
        if length < 16:
            missing = 16 - length
            for i in range(missing):
                as_string = '0' + as_string
        return as_string

    def _connect(self):
        self._socket.connect(
            (
                self._server_address,
                self._server_port
            )
        )

    def send_as_json(self, dictionary: dict):

        if not self.connection_alive:
            return None

        self._connect()
        self._send_message(
            json.dumps(dictionary)
        )

    def receive_json(self):

        if not self.connection_alive:
            return None

        self._socket.bind(
            (
                self._server_address,
                self._server_port
            )
        )

        while self.connection_alive:

            self._socket.listen(5)
            serving_socket, address = self._socket.accept()
            message = self._receive_message(serving_socket)
            serving_socket.close()
            self.close_connection()
            return json.loads(message)

        return None