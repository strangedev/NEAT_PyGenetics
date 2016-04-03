from unittest import TestCase

import time

import datetime
from unittest.mock import MagicMock

from NEAT.Logging.Logger import Logger


class TestLogger(TestCase):
    def setUp(self):
        self.logger = Logger("log")
        self.log_levels = {
            "debug": 0,
            "info": 1,
            "sig_info": 2,
            "warning": 3,
            "sig_warning": 4,
            "error": 5,
            "sig_error": 6
        }

    def test_log_levels(self):
        self.assertDictEqual(self.log_levels, self.logger.log_levels())

    def test_log_labels(self):
        for i in range(0, 7):
            self.assertEqual(i, self.log_levels.get(self.logger.log_labels()[i]))

    def test_lookup_log_level(self):
        for i in self.log_levels.keys():
            self.assertEqual(self.log_levels[i], self.logger.lookup_log_level(i))
        self.assertEqual(7, self.logger.lookup_log_level("randomShit"))

    def test_lookup_log_level_label(self):
        for i in range(0, 7):
            self.assertEqual(i, self.log_levels.get(self.logger.lookup_log_level_label(i)))

    def test_lookup_log_file(self):
        self.assertEqual("./debug.log", self.logger.lookup_log_file(0))

    def test_get_timestamp(self):
        self.assertEqual(datetime.datetime.fromtimestamp(time.time()).strftime("[%Y-%m-%d | %H:%M:%S] "),
                         self.logger.get_timestamp())

    def test_log(self):
        self.logger.log("hello", "whatever")

        self.logger.open_log = MagicMock()
        Logger.get_timestamp = MagicMock(return_value="testing")
        self.assertEqual("testing", Logger.get_timestamp())
        self.logger.log("test")
        self.logger.open_log.assert_called_with("log/./info.log", "log/./log", "testinginfo: test")

