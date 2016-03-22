import os, time, datetime


class Logger:
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

    @staticmethod
    def log_levels() -> dict:
        log_level = {}
        for i in range(0, 7):
            log_level.__setitem__(Logger.log_labels()[i], i)
        return log_level

    @staticmethod
    def log_labels() -> [str]:
        return ["debug", "info", "sig_info", "warning", "sig_warning", "error", "sig_error"]

    @staticmethod
    def lookup_log_level(log_level: str) -> int:
        return Logger.log_levels()[log_level]

    @staticmethod
    def lookup_log_level_label(log_level: int) -> str:
        return Logger.log_labels()[log_level]

    @staticmethod
    def lookup_log_file(log_level: int) -> str:
        return ("./" +
                Logger.lookup_log_level_label(log_level) +
                ".log")

    @staticmethod
    def get_timestamp():
        return datetime.datetime.fromtimestamp(time.time()).strftime("[%Y-%m-%d | %H:%M:%S] ")

    def log(self, message: str, log_level: int = 1):
        if not isinstance(type(log_level), type(1)):
            log_level = Logger.lookup_log_level(
                str(log_level)
            )
        if log_level not in range(7):
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
        message = (str(Logger.get_timestamp()) +
                   log_level_label + ": " +
                   message)
        try:
            with open(file_path, "a") as file:
                file.write(message)
                file.close()
            with open(global_log_file_name, "a") as file:
                file.write(message)
                file.close()
        except Exception:
            return
