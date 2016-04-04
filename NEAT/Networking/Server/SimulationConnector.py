from typing import Dict, List

from bson import ObjectId

from NEAT.ErrorHandling.Exceptions.NetworkProtocolException import NetworkProtocolException
from NEAT.ErrorHandling.Exceptions.NetworkTimeoutException import NetworkTimeoutException
from NEAT.GenomeStructures.StorageStructure.StorageGenome import StorageGenome
from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.Networking.Server.NEATServer import NEATServer


class SimulationConnector(object):
    """
    A class providing a high-level interface to
    a client connected via the NEATClient.
    It receives commands from NEATServer's message
    queue und responds to them.
    When a function from SimulationConnector is called,
    the client is expected to have sent a certain command
    (if there are no commands in the message queue, the Server
    will wait for the next command to be received). If the
    client has sent another command, or a command where
    the expected parameters are not present,
    NetworkProtocolException will be raised.
    """

    def __init__(self) -> None:
        self._server = NEATServer()  # type: NEATServer

    def _listen_for_command(
            self,
            command_type: str,
            parameter_filter: Dict[str, object]=None,
            timeout: int = None
    ) -> BaseCommand:
        """
        Waits for the message queue to have a command ready,
        pops the command from the queue and inspects it.
        Returns the received command if it's type and parameters
        match type / filter.
        If the next received command does not match,
        NetworkProtocolException is raised.
        :param command_type: The type of the expected command as string
        :param parameter_filter: A dictionary of parameters that are expected to be
        present in the command's parameters.
        :param timeout: The timeout after which the attempt to get
        the command will fail
        :return: The received command object
        """
        # TODO: timeouts, more error handling
        command = self._server.fetch(timeout)
        print("Received: ", command)
        if not command:
            raise NetworkTimeoutException

        if not command.type == command_type:
            self._respond_to_command(command, acknowledged=False)
            raise NetworkProtocolException("Wrong command type encountered")

        if parameter_filter:
            for key, value in parameter_filter.items():
                if key not in command.parameters.keys():
                    self._respond_to_command(command, acknowledged=False)
                    raise NetworkProtocolException("Filter key not in command parameters")
                if not value == command.parameters[key]:
                    self._respond_to_command(command, acknowledged=False)
                    raise NetworkProtocolException("Filter values do not match in command parameters")

        return command

    def _respond_to_command(
            self,
            command: BaseCommand,
            result: Dict[str, object]=None,
            acknowledged: bool=True,
            timeout: int=2000
    ) -> None:
        """
        Sends the altered command object of a previously
        received command back to the client.
        The command object that is sent back to the client
        should always be the same object that had been received
        from the client.
        the results of the command execution are passed back to client
        inside the command.result dictionary. If this dictionary
        isn't present in the passed command, it will be created.
        All commands that're passed back to the client and that
        have been handled by the server contain an 'acknowledged'
        field inside results. If this is set to true, the command
        has been executed and the networking protocol hasn't been
        breached.
        :param command: The command object that is sent back
        to the client
        :param result: The result dictionary to be attached to
        the command before it's sent back
        :param acknowledged: Whether the command has been
        acknowledged by the server
        :param timeout: The timeout after which the send operation
        will fail if the client hasn't connected yet
        :return: None
        """
        if not result:
            result = dict({})
        command.result = result
        command.result["acknowledged"] = acknowledged
        self._server.respond(command)

    def get_session(self) -> Dict[str, object]:
        """
        Awaits the AnnounceSession command to be sent by the client.
        :return: The session parameters for the new simulation session
        """
        session_command = self._listen_for_command("AnnounceSession")
        self._respond_to_command(session_command)
        return session_command.parameters

    def send_block(
            self,
            block: List[StorageGenome],
            block_id: int
    ) -> None:
        """
        Awaits the GetBlock command to be sent by the client
        and sends the block to the client.
        :param block: The List of StorageGenomes to be sent to the client
        :param block_id: The id (0 - block_count) of the block to be sent
        :return: None
        """
        block_to_send = {
            genome.object_id:
                {
                    input_label: None
                    for input_label in genome.inputs.keys()
                    }
            for genome in block
            }
        result = {
            "block": block_to_send,
            "block_id": block_id,
            "next_block_id": block_id + 1,
            "block_size": len(list(block_to_send.keys()))
        }

        get_command = self._listen_for_command("GetBlock", {"block_id": block_id})
        self._respond_to_command(
            get_command,
            result
        )

    def get_block_inputs(
            self,
            block_id: int
    ) -> Dict[ObjectId, Dict[str, float]]:
        """
        Awaits the SetInputs command to be sent by the client.
        :param block_id: The id of the block whose inputs
        should by received
        :return: The received inputs as Dictionary of
        genome_id: Dict[input_label: input_value]
        """
        set_command = self._listen_for_command("SetInputs", {"block_id": block_id})
        self._respond_to_command(set_command)
        return set_command.parameters["block"]

    def send_block_outputs(
            self,
            outputs: Dict[ObjectId, Dict[str, float]],
            block_id: int
    ) -> None:
        """
        Awaits the GetOutputs command to be sent by the client
        and sends the outputs for the previously received
        inputs back to the client.
        :param outputs: The output values as dictionary of
        genome_id: Dict[output_label: output_value]
        :param block_id: The od of the block whose inputs
        should be sent
        :return: None
        """
        get_command = self._listen_for_command("GetOutputs", {"block_id": block_id})
        get_command.result["outputs"] = outputs
        self._respond_to_command(get_command)

    def get_fitness_values(
            self,
            block_id: int
    ) -> Dict[ObjectId, float]:
        """
        Awaits the SetFitnessValues command to be sent by the client.
        :param block_id: The id of the block whose fitness values
        should be received
        :return: The received fitness values as dictionary of
        genome_id: fitness_value
        """
        set_command = self._listen_for_command(
            "SetFitnessValues",
            {
                "block_id": block_id
            }
        )
        self._respond_to_command(set_command)
        return set_command.parameters["fitness_values"]

    def get_advance_generation(self) -> bool:
        """
        Awaits the AdvanceGeneration command to be sent by the client.
        :return: A bool indicating whether the next generation should be
        calculated by NEAT (True) or the current session should be archived
        (False).
        """
        advance_command = self._listen_for_command("AdvanceGeneration")
        self._respond_to_command(advance_command)
        return advance_command.parameters["advance_generation"]
