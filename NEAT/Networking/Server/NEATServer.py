from threading import Semaphore, Thread

from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.Networking.Commands.CommandTranscoder import CommandTranscoder
from NEAT.Networking.Server.JSONSocket import JSONSocket

message_queue_size = 64
server_address = "127.0.0.1"
server_port = 8081

in_free = Semaphore(message_queue_size)
in_full = Semaphore(0)
in_mutex = Semaphore(1)

out_free = Semaphore(message_queue_size)
out_full = Semaphore(0)
out_mutex = Semaphore(1)

class QueueWorker(Thread):

    def __init__(self, queue, mode, port):
        self._queue = queue
        self._mode = mode
        self._port = port

        super().__init__()
        self.start()

    def run(self):
        while True:
            if self._mode == "recv":
                self._work_receive()
            else:
                self._work_send()

    def _work_receive(self):
        self.socket = JSONSocket(server_address, self._port)
        dictionary = self.socket.receive_dict()

        in_free.acquire()
        in_mutex.acquire()
        self._queue.append(
            CommandTranscoder.decode_command(
                dictionary
            )
        )
        in_mutex.release()
        in_full.release()

    def _work_send(self):
        self.socket = JSONSocket(server_address, server_port)
        out_full.acquire()
        out_mutex.acquire()
        command = self._queue.pop(0)
        out_mutex.release()
        out_free.release()
        self.socket.send_dict(
            CommandTranscoder.encode_command(
                command
            )
        )

class NEATServer(object):

    def __init__(self):
        self._out_queue = []
        self._in_queue = []

        self._in_queue_worker = QueueWorker(self._in_queue, "recv", server_port)
        self._out_queue_worker = QueueWorker(self._out_queue, "send", server_port + 1)

    def _enqueue_command(self, command: BaseCommand):
        out_free.acquire()
        out_mutex.acquire()
        self._out_queue.append(command)
        out_mutex.release()
        out_full.release()

    def _dequeue_command(self):
        in_full.acquire()
        in_mutex.acquire()
        command = self._in_queue.pop(0)
        in_mutex.release()
        in_free.release()
        return command

    def respond(self, command: BaseCommand):
        try:
            self._enqueue_command(command)
            return True
        except Exception as e:
            print(e)
            return False

    def fetch(self):
        try:
            return self._dequeue_command()
        except Exception as e:
            print(e)
            return None

