from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy, Duration,
    aws_sqs as sqs,
    aws_iam as iam,
    aws_s3 as s3,
    aws_sns as sns,
    aws_lambda as _lambda,
    aws_s3_notifications as s3_notify,
    aws_lambda_event_sources as event_sources,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,
    aws_sns_subscriptions as subscriptions,
    aws_dynamodb as dynamodb,
   
)
from constructs import Construct

""" Invocation Command E.g """
""" cdk deploy -c email=awesome@email.com """

class processingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        assert self.node.try_get_context('email'), "Need to run with arg;\n`cdk deploy -c email=awesome@email.com`"

        input_bucket = s3.Bucket(self, "input-",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        output_bucket = s3.Bucket(self, "output-",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        textract_lambda = _lambda.DockerImageFunction(self, 'textract-function',
            code=_lambda.DockerImageCode.from_image_asset('lambdas/textract_function/'),
            timeout=Duration.seconds(30)
        )
        
        # textract_lambda configurations
        input_bucket.grant_read(textract_lambda)
        textract_lambda.role.add_to_principal_policy(
            iam.PolicyStatement(
                actions=['textract:DetectDocumentText'],
                resources=['*'],
            )
        )
        
        comprehend_lambda = _lambda.DockerImageFunction(self, 'comprehend-function',
            code=_lambda.DockerImageCode.from_image_asset('lambdas/comprehend_function/'),
            timeout=Duration.seconds(30)
        )
        
        # Comprehend lambda configurations
        comprehend_lambda.role.add_to_principal_policy(
            iam.PolicyStatement(
                actions=['comprehend:DetectSentiment'],
                resources=['*'],
            )
        )
        
        topic = sns.Topic(self, "alert-topic")
        table = dynamodb.Table(self, "Table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        
        sns_lambda = _lambda.DockerImageFunction(self, 'sns-function',
            code=_lambda.DockerImageCode.from_image_asset('lambdas/sns_function/'),
            timeout=Duration.seconds(5),
            environment={
                'TOPIC_ARN': topic.topic_arn,
                'TABLE_NAME': table.table_name
            }
        )
        
        # topic/sns_lambda config
        topic.grant_publish(sns_lambda)
        topic.add_subscription(subscriptions.EmailSubscription(self.node.try_get_context('email')))
        
        # Define step function chain
        definition = sfn.Chain.start(
            sfn_tasks.LambdaInvoke(self, 'Invoke textract Lambda', 
                lambda_function=textract_lambda,
            )
        ).next(
            sfn_tasks.LambdaInvoke(self, 'Invoke comprehend Lambda',
                lambda_function=comprehend_lambda
            )
        ).next(
            sfn_tasks.LambdaInvoke(self, 'Invoke sns Lambda',
                lambda_function=sns_lambda
            )
        )
        
        state_machine = sfn.StateMachine(
            self, 'StateMachine',
            definition=definition,
            timeout=Duration.minutes(5)
        )
        
        #Lambda to invoke step function upon object creation
        starter_lambda = _lambda.DockerImageFunction(self, 'starter-function',
            code=_lambda.DockerImageCode.from_image_asset('lambdas/starter_function/'),
            timeout=Duration.seconds(5),
            environment={
                'STATE_MACHINE_ARN': state_machine.state_machine_arn
            }
        )
        notification = s3_notify.LambdaDestination(starter_lambda)
        input_bucket.add_object_created_notification(notification)
        
        state_machine.grant_start_execution(starter_lambda)