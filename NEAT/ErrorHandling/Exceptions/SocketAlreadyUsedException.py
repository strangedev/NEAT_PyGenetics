class SocketAlreadyUsedException(Exception):
    def __init__(self, message="", errors=None):
        super(SocketAlreadyUsedException, self).__init__(message)


