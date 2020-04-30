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
        files_to_export = [join(directory, file) for file in os.listdir(directory) if file.endswith('.gz')]
        ApplicationLogger.info(files_to_export)
        num_exported = 0
        for file_path in files_to_export:
            ApplicationLogger.info(
                "Exporting {fp} ({ne} / {tf})".format(fp=file_path, ne=++num_exported, tf=len(files_to_export)))
            self.__upload(file_path, bucket)
            if self.__delete_exported:
                os.remove(file_path)

    def __upload(self, file_path, bucket):
        try:
            object_name = file_path.split()[-1]
            self.__s3.upload_file(file_path, bucket, object_name)
        except ClientError as e:
            return ApplicationLogger.error(e)
        return True
