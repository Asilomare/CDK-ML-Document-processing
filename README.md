# CDK Application: AWS Textract and Comprehend with S3, DynamoDB and SNS

This is a Python CDK application that sets up an automated text processing pipeline. When a new file is added to an S3 bucket, it triggers a Step Function workflow, which uses AWS Textract to extract text from the document, AWS Comprehend to analyze the sentiment of the text, and finally, depending on the sentiment, publishes the result to an SNS topic.

The use case in mind when building this was as follows: Processing hand written documents (E.g surveys, feedback forums) to detect negative sentiments and notify costumer service reps to follow up with complaint.

![](https://github.com/Asilomare/CDK-ML-Document-processing/blob/main/images/pipelinediagram.png?raw=true)

## WorkFlow

- When a new object is created in the 'input_bucket', it triggers the starter_lambda function.

- The starter_lambda function starts the execution of the StateMachine/.

- The StateMachine first invokes the textract_lambda, which uses AWS Textract to extract text from the document.

- Next, it invokes the comprehend_lambda, which uses AWS Comprehend to detect the sentiment of the extracted text.

- Finally, it invokes the sns_lambda, which publishes a message with the results to an SNS Topic. Subscribers to this topic will receive an email with the results.

## Deployment

### Prerequisites
- AWS CDK installed
- AWS CLI configured with appropriate permissions
- Python 3.6 or later

### Deploying the Stack
- Clone this repository to your local machine.
- Navigate to the root directory of the project.
- Install the necessary dependencies:
`pip install -r requirements.txt`

- Bootstrap the CDK:
`cdk bootstrap`

- Deploy the stack with the cdk deploy command, replacing awesome@email.com with the email address you want to subscribe to the SNS topic:
`cdk deploy -c email=awesome@email.com`

## Cleanup

To delete the Stack:
`cdk destroy`

## Notes

- The email address you provide with the cdk deploy command is used to subscribe to the SNS Topic. A confirmation email will be sent to this address, and you must confirm the subscription to receive notifications.

- The AWS Textract and Comprehend services are used in this stack. Please be aware of the potential costs of using these services.

- The S3 buckets in this stack are configured with RemovalPolicy.DESTROY. This means that when the stack is deleted, the S3 buckets and all of their contents will be deleted as well. If you want to keep the buckets and their contents, you should change this to RemovalPolicy.RETAIN.

- New objects **CANNOT** contain spaces. The lambda will not be able to grab the file from S3.