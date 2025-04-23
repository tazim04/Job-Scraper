import json
import boto3
import os

s3 = boto3.client("s3")
BUCKET = os.environ.get("BUCKET_NAME")

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        email = body.get("email")

        if not email:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing email"})
            }

        key = f"resumes/{email}/resume.pdf"

        download_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET, 'Key': key},
            ExpiresIn=300  # URL valid for 5 minutes
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "resumeUrl": download_url
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
