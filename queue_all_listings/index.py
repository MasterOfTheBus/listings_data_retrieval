import boto3
import os


def handler(event, context):
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    bucket = os.environ['bucket']
    queue = os.environ['queue']

    response = s3.get_object(Bucket=bucket, Key='listings.csv')
    byte_data = response['Body'].read()
    str_data = byte_data.decode('utf-8')
    rows_data = str_data.split('\n')

    # Ignore the header row
    for row_str in rows_data[1:]:
        row = row_str.split(',')
        symbol = row[0]
        name = row[1]
        if should_ignore_row(symbol, name):
            print(f'ignoring symbol={symbol}, name={name}')
        else:
            print(f'queuing symbol={symbol}')
            msg = '{"symbol": "%s"}' % (symbol)
            response = sqs.get_queue_url(QueueName=queue)
            queueUrl = response['QueueUrl']
            sqs.send_message(QueueUrl=queueUrl, MessageBody=msg)

    return {
        "success": True
    }


def should_ignore_row(symbol, name):
    return '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name
