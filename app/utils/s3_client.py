import boto3
from ..config import settings

class S3Client:
    _client = None

    @classmethod
    def initialize(cls):
        if cls._client is None:
            cls._client = boto3.client(
                's3',
                region_name=settings.AWS_REGION_NAME,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
        else:
            raise Exception("S3Client is already initialized")

    @classmethod
    def get_instance(cls):
        if cls._client is None:
            raise ValueError("S3Client has not been initialized. Call `S3Client.initialize()` first.")
        return cls._client

# This should be called at application startup
def init_s3_client():
    S3Client.initialize()
