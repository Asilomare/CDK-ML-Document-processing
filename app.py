#!/usr/bin/env python3
import os

import aws_cdk as cdk

from processing_stack.docStack import processingStack


app = cdk.App()
processingStack(app, "processingStack")

app.synth()
