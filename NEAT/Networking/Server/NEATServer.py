from threading import Semaphore, Thread
import atexit
from typing import List

from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.Networking.Commands.CommandTranscoder import CommandTranscoder
from NEAT.Networking.Server.JSONSocket import JSONSocket
from NEAT.Config.StaticConfig import ServerConfig
from NEAT.Utilities import TimeUtilities

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
    """
    A thread which operates on networking message queues
    via JSONSocket in two different modes:

    1. receive
    The worker thread will accept JSONSocket connections,
    receive dictionaries, creates command objects and inserts them
    into the appropriate queue (in_queue)

    2. send
    The worker thread will wait for command objects to appear inside
    the outgoing queue (out_queue), convert them to dictionaries
    and send them to the client via a JSONSocket.
    """

    def __init__(
            self,
            queue: List[BaseCommand],
            mode: str,
            address: str,
            port: int
    ):
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
            if self._mode == "receive":
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
    """
    A message queue server that handles sending and receiving
    of command objects via the QueueWorker and JSONSocket classes.
    """

    def __init__(self):
        self._out_queue = []
        self._in_queue = []
        self._server_address = ServerConfig.server_address
        self._server_port = ServerConfig.server_port

        # TODO: receive
        self._in_queue_worker = QueueWorker(
            self._in_queue,
            "receive",
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
        """
        Puts a command that should be sent to the client into
        the outgoing message queue.
        :param command: The command to enqueue
        :return: None
        """
        out_free.acquire()
        out_mutex.acquire()
        self._out_queue.append(
            CommandTranscoder.encode_command(
                command
            )
        )
        out_mutex.release()
        out_full.release()

    def _command_available(self) -> bool:
        """
        Checks whether the in_queue contains any elements.
        :return: True if the in_queue isn't empty
        """
        in_mutex.acquire()
        available =  len(self._in_queue) > 0
        in_mutex.release()
        return available

    def _dequeue_command(self) -> BaseCommand:
        """
        Pops a command from the incoming message queue.
        :return: None
        """
        in_full.acquire()
        in_mutex.acquire()
        command = CommandTranscoder.decode_command(
            self._in_queue.pop(0)
        )
        in_mutex.release()
        in_free.release()
        return command

    def respond(
            self,
            command: BaseCommand
    ) -> bool:
        try:
            self._enqueue_command(command)
            return True
        except Exception as e:
            print(e)
            return False

    def fetch(
            self,
            timeout: int=None
    ) -> BaseCommand:
        try:
            if timeout:
                time_passed = 0
                while time_passed < timeout:
                    starting_time = TimeUtilities.millis()
                    if self._command_available():
                        return self._dequeue_command()
                    time_passed += TimeUtilities.millis() - starting_time
                return None
            return self._dequeue_command()
        except Exception as e:
            print(e)
            return None

