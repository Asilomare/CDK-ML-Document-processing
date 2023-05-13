import boto3
from os import environ

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
textract = boto3.client('textract')

def lambda_handler(event, context):
    
    print(event)
    event_bucket_name = event['Records'][0]['s3']['bucket']['name']
    event_object_key = event['Records'][0]['s3']['object']['key']
    print(event_bucket_name)
    print(event_object_key)

    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': event_bucket_name,
                'Name': event_object_key,
            }
        }
    )
    
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    
    return {
        'status_code': 200,
        'text': text,
        'event_bucket_name': event_bucket_name,
        'event_object_key': event_object_key
    }