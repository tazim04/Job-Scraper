import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
from .aws_config import s3_client, AWS_BUCKET_NAME

# Load environment variables
load_dotenv()

def upload_file_to_s3(file_obj, object_name: str) -> bool:
    """
    Uploads a file-like object to S3.

    :param file_obj: File object from Flask request (in-memory)
    :param object_name: The S3 key (e.g., "resumes/user123/resume.pdf")
    :return: True if upload was successful, False otherwise
    """
    try:
        s3_client.upload_fileobj(file_obj, AWS_BUCKET_NAME, object_name)
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False


def delete_file_from_s3(object_name: str) -> bool:
    """
    Deletes a file from S3.

    :param object_name: S3 object name to delete
    :return: True if successful, False otherwise
    """
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=object_name)
        return True
    except Exception as e:
        print(f"Error deleting file from S3: {e}")
        return False


def generate_presigned_url(object_name: str, expiration: int = 3600) -> str:
    """
    Generates a presigned URL for a file in S3 if it exists.

    :param object_name: S3 object name (e.g., "resumes/user123/resume.pdf")
    :param expiration: URL expiration time in seconds (default: 3600s = 1 hour)
    :return: Presigned URL string if file exists, None otherwise
    """
    try:
        # Check if the file exists
        s3_client.head_object(Bucket=AWS_BUCKET_NAME, Key=object_name)

        # Generate a presigned URL
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
        return url
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"File not found: {object_name}")
            return None  # File does not exist
        print(f"Error generating presigned URL: {e}")
        return None
