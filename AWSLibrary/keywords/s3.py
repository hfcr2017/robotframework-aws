from robot.api import logger
from botocore.exceptions import ClientError


class FatalError(RuntimeError):
    ROBOT_EXIT_ON_FAILURE = True

class KeywordError(RuntimeError):
    ROBOT_SUPPRESS_NAME = True

class ContinuableError(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = True


class S3Manager(object):

    def __init__(self, access_key, secret_key):
        self.bucket = None

    def list_buckets(self):
        client = self.get_client()
        if self.get_client == None:
            return "First set client"
        return client.list_buckets()

    def get_bucket(self, bname):
        logger.console(self.access_key)
        s3 = self.r_session
        if s3 == None:
            s3 = self.get_resource()
        bucket = s3.Bucket(bname)
        res = bucket in s3.buckets.all()
        if res == False:
            raise KeywordError("Bucket {} does not exist".format(bname))
        

    def get_object(self, bucket_name, obj):
        client = self.get_client()
        if self.client == None:
            client = self.get_client()
        resp = client.get_object(Bucket=bucket_name, Key=obj) 
        self._builtin.log("Returned Object: %s" % resp['Body'].read()) 

    def key_should_not_exist(self, bucket, path, key):
        client = self.client
        try:
            res = client.head_object(Bucket=bucket, Key=key)
            if res['ResponseMetadata']['HTTPStatusCode'] == 200:
                raise KeywordError("Key: {}, already exists at path: {}".format(key, path))
        except ClientError as e:
            self._builtin.log(e.response['Error']) 
            logger.console(e.response['Error'])
        return True

    def key_should_exist(self, bucket, path, key):
        client = self.client
        res = client.head_object(Bucket=bucket, Key=key)
        try:
            if res['ResponseMetadata']['HTTPStatusCode'] == 404:
                raise KeywordError("Key: {}, does not exist at path: {}".format(key, path))
        except ClientError as e:
            self._builtin.log(e.response['Error']) 
            logger.console(e.response['Error'])
        return True

    def upload_file(self, bucket, path, key):
        client = self.client
        try:
            file = client.upload_file(path, bucket, key)
        except ClientError as e:
            self._builtin.log(e.response['Error']) 
            logger.console(e.response['Error'])
        return True