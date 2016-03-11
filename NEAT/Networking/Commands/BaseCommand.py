class BaseCommand(object):

    def __init__(self):
        self._type = "BaseCommand"
        self.parameters = dict({})
        self.result = dict({})

    def from_dict(self, dictionary):
        self.__dict__ = dictionary

    def as_dict(self):
        return self.__dict__

    def __eq__(self, obj: 'BaseCommand') -> bool:
        return self._type.__eq__(obj._type) and \
            self.parameters.__eq__(obj.parameters) and \
            self.result.__eq__(obj.result)