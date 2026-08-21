import os
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url = os.getenv("SEAWEEDFS_ENDPOINT", "http://seaweedfs:8333"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
)

BUCKET_NAME = "documents"

def ensure_bucket():
    existing = [b["Name"] for b in s3.list_buckets().get("Buckets", [])]
    if BUCKET_NAME not in existing:
        s3.create_bucket(Bucket = BUCKET_NAME)
