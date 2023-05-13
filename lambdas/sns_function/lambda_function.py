import json
import boto3
from os import environ

sns = boto3.client('sns')
dynamodb = boto3.client('dynamodb')
topic_arn = environ['TOPIC_ARN']
table_name = environ['TABLE_NAME']

def lambda_handler(event, context):
    # 'event' contains the input to the function
    recipient_type = event.get('recipient_type')  # Get the recipient type from the input
    scores_dict = event['Payload']['sentiment']['SentimentScore']  # Get the message from the input
    sentiment_scores_item = {key: {'N': str(value)} for key, value in scores_dict.items()} # for dynamoDB 

    text = event['Payload']['text']
    buck = event['Payload']['event_bucket_name']
    obj = event['Payload']['event_object_key']
    
    scores = scores_dict.values()
    
    pos = scores_dict['Positive']
    neg = scores_dict['Negative']
    neu = scores_dict['Neutral']
    
    # Check if negative is the greatest value in tuple /
    # Check if sentiment is negative
    sns_response = False
    if neg == max(scores): 
        message = f"Negative statement detected at:\nBucket: {buck}\nKey:{obj}"
        
        # Publish the message to the SNS Topic
        sns_response = sns.publish(
            TopicArn=topic_arn,
            Message=message
        )
    elif pos == max(scores):
        #Do something else if positive
        pass
    else:
        # Do something else if neutral
        pass
    
    db_response = dynamodb.put_item(
        TableName=table_name,  # Replace with your table name
        Item={
            's3_bucket': {'S': buck},
            's3_obj': {'S': obj},
            'text': {'S': text},
            'sentiment': {'M': sentiment_scores_item},
        }
    )

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully stored data in DynamoDB, Message {"Sent" if sns_response else "Not Sent"}'),
    }