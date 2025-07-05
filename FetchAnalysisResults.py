import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #Configuration
    bucket = 'ai-image-upload-bucket1'
    allowed_extensions = ['.json']  #Only allow fetching JSON files
    
    try:
        #Validate input
        params = event.get('queryStringParameters', {}) or {}
        filename = params.get('filename', '').strip()
        
        if not filename:
            return error_response(400, 'Filename parameter is required')
            
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            return error_response(400, 'Only JSON files are allowed')
        
        #Sanitize filename and construct key
        sanitized_filename = ''.join(c for c in filename if c.isalnum() or c in ('-', '_', '.'))
        key = f'results/{sanitized_filename}'
        
        #Fetch from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        #Validate JSON content
        json.loads(content)  # Will raise ValueError if invalid
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'max-age=300'  #Cache for 5 minutes
            },
            'body': content
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NoSuchKey':
            return error_response(404, 'Result not found')
        elif error_code == 'AccessDenied':
            return error_response(403, 'Access denied')
        return error_response(500, 'S3 service error')
        
    except ValueError:
        return error_response(400, 'Invalid JSON content')
        
    except Exception as e:
        return error_response(500, 'Internal server error')

def error_response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'error': message})
    }