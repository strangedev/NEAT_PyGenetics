from NEAT.ErrorHandling.Exceptions.SerializationException import SerializationException
from NEAT.ErrorHandling.Exceptions.SocketRuntimeException import SocketRuntimeException
from NEAT.ErrorHandling.Exceptions.SocketAlreadyUsedException import SocketAlreadyUsedException
import socket
import json
from threading import Thread

class JSONSocket(Thread):

    def __init__(
        self,
        server_address,
        server_port,
        header_size=16,
        chunk_size=1024
    ):
        super().__init__()

        self._socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self._socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self._server_address = server_address
        self._server_port = server_port
        self._header_size = header_size
        self._chunk_size = chunk_size
        self._socket_alive = True

    @property
    def socket_alive(self):
        return self._socket_alive

    def close_connection(self):
        if self.socket_alive:
            self._socket.close()
            self._socket_alive = False

    def _receive_message(self, socket: socket.socket):

        message_size = self._receive_message_size(socket)

        message_chunks = []
        bytes_received = 0

        while bytes_received < message_size:
            chunk = socket.recv(
                min(
                    message_size - bytes_received,
                    self._chunk_size
                )
            )
            if chunk == "":
                raise RuntimeError("JSONSocket: socket broken")
            message_chunks.append(chunk.decode('utf-8'))
            bytes_received += len(chunk)

        return ''.join(message_chunks)

    def _receive_message_size(self, socket: socket.socket):

        message_size_chunks = []
        bytes_received = 0

        while bytes_received < self._header_size:
            chunk = socket.recv(
                min(
                    self._header_size - bytes_received,
                    self._header_size
                )
            )
            if chunk == '':
                raise RuntimeError("JSONSocket: socket broken")
            message_size_chunks.append(chunk.decode('utf-8'))
            bytes_received += len(chunk)

        return int(''.join(message_size_chunks))

    def _send_message(self, message: str):

        message_size = len(message)
        bytes_sent = 0

        message_size_serialized  = self._serialize_message_size(message_size)

        while bytes_sent < self._header_size:
            sent = self._socket.send(
                message_size_serialized[bytes_sent:]
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

    def _serialize_message_size(self, message_size: int):
        if message_size > 10**self._header_size:
            raise SerializationException(
                "The message length exceeded the header size ("
                + str(self._header_size)
                + ")"
            )
        as_string = str(message_size)
        length = len(as_string)
        if length < self._header_size:
            missing = self._header_size - length
            for i in range(missing):
                as_string = '0' + as_string
        return as_string.encode('utf-8')

    def _serialize_dict(self, dictionary: dict):
        return json.dumps(dictionary).encode('utf-8')

    def _deserialize_dict(self, string: str):
        return json.loads(string)

    def _connect(self):
        self._socket.connect(
            (
                self._server_address,
                self._server_port
            )
        )

    def send_dict(self, dictionary: dict):

        try:
            if not self.socket_alive:
                raise SocketAlreadyUsedException

            self._connect()
            self._send_message(
                json.dumps(dictionary).encode('utf-8')
            )
            self.close_connection()
        except RuntimeError:
            raise SocketRuntimeException(
                "Runtime error encountered while sending dictionary."
            )
        finally:
            self.close_connection()

    def receive_dict(self):

        try:
            if not self.socket_alive:
                raise SocketAlreadyUsedException

            self._socket.bind(
                (
                    self._server_address,
                    self._server_port
                )
            )

            while self.socket_alive:

                self._socket.listen(5)
                serving_socket, address = self._socket.accept()
                dictionary = self._receive_message(serving_socket)
                serving_socket.close()
                return self._deserialize_dict(dictionary)
        except RuntimeError:
            raise SocketRuntimeException(
                "Runtime error encountered while receiving dictionary."
            )
        finally:
            self.close_connection()