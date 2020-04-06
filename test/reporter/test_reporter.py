import unittest
from unittest import mock
from unittest.mock import Mock, PropertyMock

from roadnoise.poller.poller import Poller
from roadnoise.reporter.reporter import Reporter


class TestReporter(unittest.TestCase):
    POLLED_VALUE = 'polled value'

    @mock.patch('roadnoise.poller.poller.Poller.value', new_callable=PropertyMock)
    def test_report(self, mock_poller_value):
        device = Mock()
        poller = Poller(device, 1)
        mock_poller_value.return_value = self.POLLED_VALUE
        logger = Mock()

        reporter = Reporter([poller, poller], logger, 1)
        reporter.start()
        reporter.stop()

        logger.log.assert_called_with([self.POLLED_VALUE, self.POLLED_VALUE])

    @mock.patch('roadnoise.poller.poller.Poller.value', new_callable=PropertyMock)
    def test_report_invalid_value(self, mock_poller_value):
        device = Mock()
        poller = Poller(device, 1)
        mock_poller_value.return_value = None

        logger = Mock()

        reporter = Reporter([poller, poller], logger, 1)
        reporter.start()
        reporter.stop()

        logger.log.assert_not_called()
