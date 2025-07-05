import json
import boto3
from botocore.client import Config
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        #Input validation
        if not event.get('queryStringParameters') or not event['queryStringParameters'].get('filename'):
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'filename parameter is required'})
            }

        bucket = 'ai-image-upload-bucket1'
        file_name = event['queryStringParameters']['filename']
        
        #Sanitize filename to prevent path traversal
        safe_file_name = file_name.replace('../', '').replace('..\\', '')
        object_name = f"input/{safe_file_name}"

        #Initialize S3 client with explicit signature version
        s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
        
        #Generate presigned URL
        url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': object_name,
                'ContentType': 'image/jpeg'
            },
            ExpiresIn=3600,
            HttpMethod='PUT'
        )

        logger.info(f"Generated presigned URL for {object_name}")

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'uploadURL': url,
                'objectName': object_name,
                'expiresIn': 3600
            })
        }

    except Exception as e:
        logger.error(f"Error generating presigned URL: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }