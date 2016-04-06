from NEAT.Networking.Commands.BaseCommand import BaseCommand
from NEAT.Networking.Commands.AnnounceSessionCommand import AnnounceSessionCommand
from NEAT.Networking.Commands.GetBlockCommand import GetBlockCommand
from NEAT.Networking.Commands.SetInputsCommand import SetInputsCommand

class CommandTranscoder(object):

    type_class_map = dict(
        {
            "BaseCommand": BaseCommand,
            "AnnounceSession": AnnounceSessionCommand,
            "GetBlock": GetBlockCommand,
            "SetInputs": SetInputsCommand
        }
    )


    @staticmethod
    def encode_command(command: BaseCommand):
        return command.as_dict()

    @staticmethod
    def decode_command(dictionary: dict):
        if not "_type" in dictionary.keys():
            return None
        command_class = CommandTranscoder.type_class_map[dictionary["_type"]]
        command = command_class()

        command.from_dict(dictionary)
        return command