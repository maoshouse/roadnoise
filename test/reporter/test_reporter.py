import unittest
from unittest.mock import Mock

from roadnoise.reporter.reporter import Reporter


class TestReporter(unittest.TestCase):

    def test_report(self):
        device = Mock()
        logger = Mock()

        reporter = Reporter("reporter", device, logger)

        reporter.report()

        device.read.assert_called()
        logger.log.assert_called()
