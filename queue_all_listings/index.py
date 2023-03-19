import boto3
import os


def handler(event, context):
    s3 = boto3.client('s3')
    sqs = boto3.client('sqs')
    ddb = boto3.client('dynamodb')
    bucket = os.environ['bucket']
    table = os.environ['table']

    queue_url = get_queue_info(ddb, sqs, table)

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
            sqs.send_message(QueueUrl=queue_url, MessageBody=msg)

    return {
        "success": True
    }


def get_queue_info(ddb, sqs, table):
    recv_q_item = ddb.get_item(TableName=table, Key={
        'queue': {'S': 'receive_queue'}})
    recv_q_name = recv_q_item['Item']['name']['S']
    print(f'Queue is {recv_q_name}')
    response = sqs.get_queue_url(QueueName=recv_q_name)
    return response['QueueUrl']


def should_ignore_row(symbol, name):
    return '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name
