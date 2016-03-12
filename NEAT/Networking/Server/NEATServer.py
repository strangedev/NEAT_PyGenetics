from threading import Semaphore, Thread
import atexit

from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.Networking.Commands.CommandTranscoder import CommandTranscoder
from NEAT.Networking.Server.JSONSocket import JSONSocket
from NEAT.Config.StaticConfig import ServerConfig

message_queue_size = 64

in_free = Semaphore(message_queue_size)
in_full = Semaphore(0)
in_mutex = Semaphore(1)

out_free = Semaphore(message_queue_size)
out_full = Semaphore(0)
out_mutex = Semaphore(1)

thread_should_end = False
thread_should_end_mutex = Semaphore(1)

def signal_thread_should_end():
    thread_should_end_mutex.acquire()
    global thread_should_end
    thread_should_end = True
    thread_should_end_mutex.release()

atexit.register(signal_thread_should_end)

class QueueWorker(Thread):

    def __init__(self, queue, mode, address, port):
        self._queue = queue
        self._mode = mode
        self._address = address
        self._port = port

        super().__init__()
        self.start()

    def run(self):
        while True:
            if thread_should_end_mutex.acquire(timeout=1000): # TODO: put socket in timeout mode
                if thread_should_end:
                    return
                thread_should_end_mutex.release()
            if self._mode == "recv":
                self._work_receive()
            else:
                self._work_send()

    def _work_receive(self):
        self.socket = JSONSocket(self._address, self._port)
        message = self.socket.receive_dict()

        in_free.acquire()
        in_mutex.acquire()
        self._queue.append(message)
        in_mutex.release()
        in_full.release()

    def _work_send(self):
        self.socket = JSONSocket(self._address, self._port)

        out_full.acquire()
        out_mutex.acquire()
        message = self._queue.pop(0)
        out_mutex.release()
        out_free.release()

        self.socket.send_dict(message)

class NEATServer(object):

    def __init__(self):
        self._out_queue = []
        self._in_queue = []
        self._server_address = ServerConfig.server_address
        self._server_port = ServerConfig.server_port

        self._in_queue_worker = QueueWorker(
            self._in_queue,
            "recv",
            self._server_address,
            self._server_port
        )
        self._out_queue_worker = QueueWorker(
            self._out_queue,
            "send",
            self._server_address,
            self._server_port + 1
        )

    def _enqueue_command(self, command: BaseCommand):
        out_free.acquire()
        out_mutex.acquire()
        self._out_queue.append(
            CommandTranscoder.encode_command(
                command
            )
        )
        out_mutex.release()
        out_full.release()

    def _dequeue_command(self):
        in_full.acquire()
        in_mutex.acquire()
        command = CommandTranscoder.decode_command(
            self._in_queue.pop(0)
        )
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

