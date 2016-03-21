class StartupCheckException(Exception):
    def __init__(self, message="", errors=None):
        super(StartupCheckException, self).__init__(message)