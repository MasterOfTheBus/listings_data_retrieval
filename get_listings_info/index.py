import boto3
import requests
import os


def handler(event, context):
    s3 = boto3.client('s3')
    ddb = boto3.client('dynamodb')
    bucket = os.environ['bucket']
    rate_table = os.environ['rateTable']
    symbols_table = os.environ['symbolsTable']
    api_key = os.environ['apiKey']
    base_url = 'https://www.alphavantage.co'
    query_types = [
        'OVERVIEW', 'INCOME_STATEMENT', 'BALANCE_SHEET',
        'CASH_FLOW', 'EARNINGS'
    ]
    symbol = event['symbol']

    for type in query_types:
        try:
            get_query_type_and_store(s3, bucket, base_url,
                                     api_key, type, symbol)
        except RuntimeError:
            raise

    next = get_next_symbol(ddb, symbols_table, symbol)

    update_rate_limit(ddb, rate_table)

    return {
        'queue_empty': next == '',
        'symbol': next
    }


def get_next_symbol(ddb, table, current_symbol):
    response = ddb.get_item(TableName=table, Key={
        'symbol': {'S': current_symbol}
    })
    return response['Item']['next']['S']


def get_query_type_and_store(s3, bucket, base_url, api_key, type, listing):
    URL = f'{base_url}/query?function={type}&symbol={listing}&apikey={api_key}'
    with requests.Session() as s:
        download = s.get(URL)
        if download.status_code % 200 > 100:
            raise RuntimeError(
                f'Failed request: type={type}, code={download.status_code}')

        s3.put_object(
            Bucket=bucket, Key=f'{listing}/{type}.json', Body=download.content)


def update_rate_limit(ddb, rate_table):
    ddb.update_item(TableName=rate_table, Key={'Type': {'S': 'daily'}},
                    ExpressionAttributeNames={'#C': 'Count'},
                    ExpressionAttributeValues={':count': {'N': '5'}},
                    UpdateExpression='SET #C=#C+:count')
