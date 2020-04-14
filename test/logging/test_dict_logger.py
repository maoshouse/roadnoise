import unittest
from unittest import mock
from unittest.mock import Mock

from roadnoise.logging.dict_logger import DictLogger


class TestDictLogger(unittest.TestCase):
    POLLED_VALUES = [{'key1': 'value1'}, {'key2': 'value2'}]
    INVALID_POLLED_VALUES = [{'key1': 'value1'}, None]
    TIME_NS = 1586246916423931000
    EXPECTED_RECORD = {
        'key1': 'value1',
        'key2': 'value2',
        'time': TIME_NS // 1000
    }

    @mock.patch("time.time_ns", Mock(return_value=TIME_NS))
    @mock.patch("logging.Logger.info")
    def test_log(self, mock_log_info):
        logger = DictLogger("logger", None)
        logger.log(self.POLLED_VALUES)
        mock_log_info.assert_called_with(self.EXPECTED_RECORD)

    @mock.patch("time.time_ns", Mock(return_value=TIME_NS))
    @mock.patch("logging.Logger.info")
    def test_log(self, mock_log_info):
        logger = DictLogger("logger", None)
        logger.log(self.INVALID_POLLED_VALUES)
        mock_log_info.assert_not_called()
