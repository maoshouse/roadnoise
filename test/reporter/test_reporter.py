import unittest
from unittest.mock import Mock

from roadnoise.reporter.reporter import Reporter


class TestReporter(unittest.TestCase):

    def test_report(self):
        poller = Mock()
        logger = Mock()

        reporter = Reporter("reporter", poller, logger)

        reporter.report()

        poller.poll.assert_called()
        logger.log.assert_called()
