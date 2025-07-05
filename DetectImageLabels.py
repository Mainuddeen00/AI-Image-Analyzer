import json
import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        #Get bucket & key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        print(f"Bucket: {bucket}")
        print(f"Key: {key}")

        #Confirm the file exists (prevents InvalidS3ObjectException)
        try:
            s3.head_object(Bucket=bucket, Key=key)
            print("✅ File exists in S3.")
        except Exception as e:
            print(f"❌ File does not exist or no permission: {str(e)}")
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'File not found in S3 or access denied.'})
            }

        #Call Rekognition
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=10
        )

        labels = response['Labels']
        print(f"✅ Detected labels for {key}:")
        for label in labels:
            print(f"{label['Name']} : {round(label['Confidence'], 2)}%")

        #Save results to results/ folder
        result_key = 'results/' + key.split('/')[-1] + '.json'
        s3.put_object(
            Bucket=bucket,
            Key=result_key,
            Body=json.dumps(labels, indent=2),
            ContentType='application/json'
        )
        print(f"✅ Saved results to: {result_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Success', 'results': labels})
        }

    except Exception as e:
        print(f"❌ Lambda error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
