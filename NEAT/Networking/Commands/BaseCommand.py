class BaseCommand(object):

    def __init__(self):
        self._type = "BaseCommand"
        self.parameters = dict({})
        self.result = dict({})

    def from_dict(self, dictionary):
        self.__dict__ = dictionary

    def as_dict(self):
        return self.__dict__

    @property
    def acknowledged(self):
        ack = self._get_result_if_exists("acknowledged")
        return ack if ack else False

    @property
    def type(self):
        return self._type

    def _get_result_if_exists(self, key):
        if key in self.result.keys():
            return self.result[key]
        return None

    def __eq__(self, obj: 'BaseCommand') -> bool:
        return self._type.__eq__(obj._type) and \
            self.parameters.__eq__(obj.parameters) and \
            self.result.__eq__(obj.result)
