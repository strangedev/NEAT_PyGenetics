class NetworkTimeoutException(Exception):
    def __init__(self, message="", errors=None):
        super(NetworkTimeoutException, self).__init__(message)


