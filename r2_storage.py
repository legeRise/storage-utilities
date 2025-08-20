import boto3
import os
from botocore.client import Config

import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv(override=True)


class R2Storage:
    def __init__(
        self,
        bucket_name=None,
        endpoint_url=None,
        access_key=None,
        secret_key=None
    ):
        self.bucket = bucket_name or os.getenv("R2_BUCKET_NAME")
        self.endpoint = (endpoint_url or os.getenv("R2_ENDPOINT_URL")).rstrip('/')
        print(self.bucket,'is the bucket')
        print(endpoint_url,'is the endpoint url')
        self.r2 = boto3.client(
            's3',
            aws_access_key_id=access_key or os.getenv("R2_ACCESS_KEY_ID"),
            aws_secret_access_key=secret_key or os.getenv("R2_SECRET_ACCESS_KEY"),
            endpoint_url=self.endpoint,
            region_name='auto',
            config=Config(signature_version='s3v4')
        )

    # ✅ List files under a prefix
    def list_files(self, prefix=""):
        resp = self.r2.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [obj['Key'] for obj in resp.get('Contents', [])]
    
    def list_files_with_times(self, prefix=""):
        resp = self.r2.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [
            {"Key": obj['Key'], "LastModified": obj['LastModified']}
            for obj in resp.get('Contents', [])
        ]

    # ✅ Delete a file
    def delete(self, key):
        self.r2.delete_object(Bucket=self.bucket, Key=key)
        return True

    # ✅ Get a public or signed view URL
    def get_view_url(self, key, expires_in=3600):
        return self.r2.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': key},
            ExpiresIn=expires_in
        )
        
    def clear_bucket(self):
        paginator = self.r2.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket):
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    self.delete(key)

    # ✅ Generate signed upload URL (frontend will use this to PUT directly)
    def generate_upload_url(self, key, content_type="application/octet-stream", expires_in=3600):
        return self.r2.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': self.bucket,
                'Key': key,
                'ContentType': content_type
            },
            ExpiresIn=expires_in
        )

    # ✅ Upload from backend (Django job, not browser) — with optional public ACL
    def upload_file(self, key, file_path, content_type=None):
        extra = {}
        if content_type:
            extra['ContentType'] = content_type

        self.r2.upload_file(
            Filename=file_path,
            Bucket=self.bucket,
            Key=key,
            ExtraArgs=extra
        )
        return self.get_view_url(key)

    # ✅ Check if object exists
    def exists(self, key):
        try:
            self.r2.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise



if __name__ == '__main__':
    r2_bucket = R2Storage(
        bucket_name='ezclip-db-backups')
    print(r2_bucket.list_files_with_times())

    

    
    
