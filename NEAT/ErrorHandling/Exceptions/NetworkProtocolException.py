class NetworkProtocolException(Exception):
    def __init__(self, message, errors=None):
        super(NetworkProtocolException, self).__init__(message)


