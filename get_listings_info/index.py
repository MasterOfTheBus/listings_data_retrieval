import boto3
import requests
import os

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
ddb = boto3.client('dynamodb')
bucket = os.environ['bucket']
table = os.environ['table']
retrieval_table = os.environ['retrievalTable']
api_key = os.environ['apiKey']
base_url = 'https://www.alphavantage.co'
query_types = [
    'OVERVIEW', 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW', 'EARNINGS'
]


def handler(event, context):

    queue_url = get_queue_info(ddb, sqs, retrieval_table)
    response = sqs.receive_message(QueueUrl=queue_url,
                                   WaitTimeSeconds=20)
    messages = response['Messages']
    if len(messages) == 0:
        return {'queue_empty': True}
    message = response['Messages'][0]
    symbol = message['Body']['symbol']

    for type in query_types:
        try:
            get_query_type_and_store(type=type, listing=symbol)
        except RuntimeError:
            raise

    ddb.update_item(TableName=table, Key={'Type': {'S': 'daily'}},
                    ExpressionAttributeNames={'#C': 'Count'},
                    ExpressionAttributeValues={':count': {'N': '5'}},
                    UpdateExpression='SET #C=#C+:count')

    return {
        "queue_empty": False
    }


def get_queue_info(ddb, sqs, table):
    recv_q_item = ddb.get_item(TableName=table, Key={
        'queue': {'S': 'receive_queue'}})
    recv_q_name = recv_q_item['Item']['name']['S']
    print(f'Queue is {recv_q_name}')
    response = sqs.get_queue_url(QueueName=recv_q_name)
    return response['QueueUrl']


def get_query_type_and_store(type, listing):
    URL = f'{base_url}/query?function={type}&symbol={listing}&apikey={api_key}'
    with requests.Session() as s:
        download = s.get(URL)
        if download.status_code % 200 > 100:
            raise RuntimeError(
                f'Failed request: type={type}, code={download.status_code}')

        s3.put_object(
            Bucket=bucket, Key=f'{listing}/{type}.json', Body=download.content)
