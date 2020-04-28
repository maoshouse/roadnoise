import unittest
from unittest import mock
from unittest.mock import Mock

from botocore.exceptions import ClientError

from roadnoise.exporter.s3_exporter import S3Exporter


class TestS3Exporter(unittest.TestCase):

    @mock.patch("boto3.Session")
    @mock.patch("os.listdir")
    @mock.patch("os.remove")
    def test_export(self, mock_remove, mock_listdir, mock_session):
        listed_files = ['log1.gz', 'log2.gz']
        mock_listdir.return_value = listed_files
        session_instance = Mock()
        mock_session.return_value = session_instance
        s3 = session_instance.client()

        S3Exporter().export("dir", "bucket")
        self.assertEqual(len(listed_files), s3.upload_file.call_count)
        mock_remove.assert_not_called()

    @mock.patch("boto3.Session")
    @mock.patch("os.listdir")
    @mock.patch("os.remove")
    def test_export_and_delete(self, mock_remove, mock_listdir, mock_session):
        listed_files = ['log1.gz', 'log2.gz']
        mock_listdir.return_value = listed_files
        session_instance = Mock()
        mock_session.return_value = session_instance
        s3 = session_instance.client()

        S3Exporter(delete_exported=True).export("dir", "bucket")
        self.assertEqual(len(listed_files), s3.upload_file.call_count)
        self.assertEqual(len(listed_files), mock_remove.call_count)

    @mock.patch("boto3.Session")
    @mock.patch("os.listdir")
    @mock.patch("os.remove")
    def test_export_partial_failure(self, mock_remove, mock_listdir, mock_session):
        listed_files = ['log1.gz', 'log2.gz']
        mock_listdir.return_value = listed_files
        session_instance = Mock()
        mock_session.return_value = session_instance
        s3 = session_instance.client()
        s3.upload_file = Mock(
            side_effect=["good_response", ClientError(error_response={}, operation_name='bad_response')])
        S3Exporter(delete_exported=True).export("dir", "bucket")
        self.assertEqual(len(listed_files), s3.upload_file.call_count)
        mock_remove.assert_called_once()

    @mock.patch("boto3.Session")
    @mock.patch("os.listdir")
    @mock.patch("os.remove")
    def test_export_failure(self, mock_remove, mock_listdir, mock_session):
        listed_files = ['log1.gz', 'log2.gz']
        mock_listdir.return_value = listed_files
        session_instance = Mock()
        mock_session.return_value = session_instance
        s3 = session_instance.client()
        s3.upload_file = Mock(
            side_effect=ClientError(error_response={}, operation_name='bad_response'))
        S3Exporter(delete_exported=True).export("dir", "bucket")
        self.assertEqual(len(listed_files), s3.upload_file.call_count)
        mock_remove.assert_not_called()
