FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task

COPY textract_function.py .

RUN pip3 install boto3

CMD ["textract_function.lambda_handler"]