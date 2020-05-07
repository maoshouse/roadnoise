import os
from os.path import join

import boto3
from botocore.exceptions import ClientError

from roadnoise.logging.application_logger import ApplicationLogger


class S3Exporter:
    def __init__(self, delete_exported=False):
        session = boto3.Session(profile_name='roadnoise')
        self.__s3 = session.client('s3')
        self.__delete_exported = delete_exported

    def export(self, directory, bucket):
        ApplicationLogger.info("Exporting to bucket {b}".format(b=bucket))
        files_to_export = [join(directory, file) for file in os.listdir(directory)]
        ApplicationLogger.info(files_to_export)
        file_counter = 1
        for file_path in files_to_export:
            ApplicationLogger.info(
                "Exporting {fp} ({fc} / {tf})".format(fp=file_path, fc=file_counter, tf=len(files_to_export)))
            upload_success = self.__upload(file_path, bucket)
            file_counter += 1
            if upload_success and self.__delete_exported:
                os.remove(file_path)

    def __upload(self, file_path, bucket):
        try:
            object_name = file_path.split()[-1]
            self.__s3.upload_file(file_path, bucket, object_name)
            return True
        except ClientError as e:
            ApplicationLogger.error(e)
        return False
