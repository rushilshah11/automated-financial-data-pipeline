import boto3
from app.settings import settings

class S3Client:

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME
        )
        self.bucket_name = settings.S3_BUCKET_NAME
    
    def upload_log(self, key: str, data: bytes) -> str:
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                key=key,
                body=data,
                ContentType='application/json'
            )

            return f"s3://{self.bucket_name}/{key}"
        except Exception as e:
            return f"S3_UPLOAD_FAILED: {e}"
