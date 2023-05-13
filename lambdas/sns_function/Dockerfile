FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task

COPY lambda_function.py .

RUN pip3 install boto3

CMD ["lambda_function.lambda_handler"]