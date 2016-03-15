class SerializationException(Exception):
    def __init__(self, message="", errors=None):
        super(SerializationException, self).__init__(message)


