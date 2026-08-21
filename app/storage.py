import os
import time
import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("SEAWEEDFS_ENDPOINT", "http://seaweedfs:8333"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "any"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "any"),
)

BUCKET_NAME = "documents"


def ensure_bucket(retries: int = 10, delay: int = 2):
    """Create the bucket if it does not exist, waiting for SeaweedFS to be ready."""
    for attempt in range(retries):
        try:
            s3.create_bucket(Bucket=BUCKET_NAME)
            return
        except ClientError as e:
            if e.response["Error"]["Code"] in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
                return
            raise
        except EndpointConnectionError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)
