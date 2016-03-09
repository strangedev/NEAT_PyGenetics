class BaseCommand(object):

    def __init__(self):
        self._type = "BaseCommand"

    def from_dict(self, dictionary):
        self.__dict__ = dictionary

    def as_dict(self):
        return self.__dict__