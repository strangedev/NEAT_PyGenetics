class InputMissingException(Exception):
    def __init__(self, message, errors=None):
        super(InputMissingException, self).__init__(message)


