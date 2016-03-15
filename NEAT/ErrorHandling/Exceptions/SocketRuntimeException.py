class SocketRuntimeException(Exception):
    def __init__(self, message="", errors=None):
        super(SocketRuntimeException, self).__init__(message)


