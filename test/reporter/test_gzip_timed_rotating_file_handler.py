import unittest
from unittest import mock

from roadnoise.reporter.gzip_timed_rotating_file_handler import GzipTimedRotatingFileHandler


class TestGzipTimedRotatingFileHandler(unittest.TestCase):

    # TODO refactor so that either the log files are made and tested then deleted OR mock everything so that no files
    #  are created
    @mock.patch("logging.handlers.TimedRotatingFileHandler.doRollover")
    @mock.patch("os.listdir")
    def test_doRollover(self, mock_listdir, mock_timed_rotating_file_handler_doRollover):
        mock_listdir.return_value = []
        file_handler = GzipTimedRotatingFileHandler(file_name_prefix="", log_root="logroot",
                                                    when="S", interval=0, backup_count=0)
        file_handler.doRollover()
        mock_timed_rotating_file_handler_doRollover.assert_called()
