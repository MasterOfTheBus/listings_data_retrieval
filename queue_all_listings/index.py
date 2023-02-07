import boto3
import os
import csv


def handler(event, context):
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    bucket = os.environ['bucket']
    queue = os.environ['queue']

    filename = 'temp_file.csv'
    response = s3.get_object(Bucket=bucket, Key='listings.csv')
    with open(filename, 'wb') as f:
        f.write(response['body'].read())

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            symbol = row['symbol']
            if should_ignore_row(row):
                print(f'ignoring symbol={symbol}, name={row["name"]}')
            else:
                print(f'queuing symbol={symbol}')
                msg = {'symbol': symbol}
                response = sqs.get_queue_url(QueueName=queue)
                queueUrl = response['QueueUrl']
                sqs.send_message(QueueUrl=queueUrl, MessageBody=msg)

    return {
        "success": True
    }


def should_ignore_row(row):
    symbol = row['symbol']
    name = row['name']
    return '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name
