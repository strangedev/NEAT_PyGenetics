import os, time, datetime

class Logger():
    """
    Logs messages to different files, based
    on the reported log level.

    Log levels:

    0 - Debug
    1 - Info
    2 - Significant Info
    3 - Warning
    4 - Significant Warning
    5 - Error
    6 - Significant Error
    """
    def __init__(self, logging_path):
        self._logging_path = logging_path

    @property
    @staticmethod
    def log_levels():
        return {
            "debug": 0,
            "info": 1,
            "sig_info": 2,
            "warning": 3,
            "sig_warning": 4,
            "error": 5,
            "sig_error": 6
        }

    @staticmethod
    def lookup_log_level(log_level: str) -> int:
        return Logger.log_levels[log_level]

    @staticmethod
    def lookup_log_level_label(log_level: int) -> str:
        return {v: k for k, v in Logger.log_levels}[log_level]

    @staticmethod
    def lookup_log_file(log_level: int) -> str:
        return ("./"
                + Logger.lookup_log_level_label(log_level)
                + ".log")

    @staticmethod
    def get_timestamp():
        return datetime.datetime.fromtimestamp(time.time()).strftime("[%Y-%m-%d | %H:%M:%S] ")

    def log(self, message: str, log_level: int=1):
        if not type(log_level) == type(1):
            log_level = Logger.lookup_log_level(
                log_level
            )
        if not log_level in range(7):
            return
        log_level_label = Logger.lookup_log_level_label(log_level)
        log_file_name = Logger.lookup_log_file(log_level)
        file_path = os.path.join(
            self._logging_path,
            log_file_name
        )
        global_log_file_name = os.path.join(
            self._logging_path,
            "./log"
        )
        message = (Logger.get_timestamp()
                   + log_level_label + ": "
                   + message)
        try:
            with open(file_path, "a") as file:
                file.write(message)
            with open(global_log_file_name, "a") as file:
                file.write(message)
        except Exception:
            return
