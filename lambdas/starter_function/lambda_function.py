import json
import boto3
import os

def lambda_handler(event, context):
    sfn = boto3.client('stepfunctions')
    state_machine_arn = os.environ['STATE_MACHINE_ARN']

    response = sfn.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(event)
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Step Function started!')
    }

