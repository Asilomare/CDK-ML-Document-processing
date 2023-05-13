import sys
import boto3
import json

client = boto3.client('comprehend')

def lambda_handler(event, context):
    comprehend = boto3.client('comprehend')

    # Extract the text from the event
    text = event['Payload']['text']

    # Use Comprehend to analyze the sentiment of the text
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'  # Replace with the appropriate language code if not English
    )
    
    # Return the sentiment
    return {
        'statusCode': 200,
        'sentiment': response,
        'event_object_key': event['Payload']['event_object_key'],
        'event_bucket_name': event['Payload']['event_bucket_name'],
        'text': text
    }