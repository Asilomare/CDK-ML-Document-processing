import aws_cdk as core
import aws_cdk.assertions as assertions

from doc_proc.doc_proc_stack import DocProcStack

# example tests. To run these tests, uncomment this file along with the example
# resource in doc_proc/doc_proc_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DocProcStack(app, "doc-proc")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
