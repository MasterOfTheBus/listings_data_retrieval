import boto3
import requests
import os

s3 = boto3.client('s3')
bucket = os.environ['bucket']
api_key = os.environ['apiKey']
base_url = 'https://www.alphavantage.co'
query_types = [
    'OVERVIEW', 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW', 'EARNINGS'
]


def handler(event, context):

    for type in query_types:
        try:
            get_query_type_and_store(type=type, listing=event['listing'])
        except RuntimeError:
            raise

    return {
        "success": True
    }


def get_query_type_and_store(type, listing):
    URL = f'{base_url}/query?function={type}&symbol={listing}&apikey={api_key}'
    with requests.Session() as s:
        download = s.get(URL)
        if download.status_code % 200 > 100:
            raise RuntimeError(
                f'Failed request: type={type}, code={download.status_code}')

        s3.put_object(
            Bucket=bucket, Key=f'{listing}/{type}.json', Body=download.content)
