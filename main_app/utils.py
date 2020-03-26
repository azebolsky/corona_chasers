import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'coronachaser'
DEFAULT_URL = f'{S3_BASE_URL}{BUCKET}/default.png'


def upload_file(file):
    key = uuid.uuid4().hex[:6] + file.name[file.name.rfind('.'):]
    s3 = boto3.client('s3')
    s3.upload_fileobj(file, BUCKET, key)
    url = f'{S3_BASE_URL}{BUCKET}/{key}'
    return url


def delete_file(url):
    if url != DEFAULT_URL:
        key = url.rsplit('/', 1)[-1]
        s3 = boto3.client('s3')
        s3.delete_object(Bucket=BUCKET, Key=key)
    return
