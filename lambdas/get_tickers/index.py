import boto3
import os
import requests
import csv
import json


def handler(event, context):
    sfn = boto3.client('stepfunctions')
    secretsmanager = boto3.client('secretsmanager')
    stateMachineArn = os.environ['stateMachineArn']
    secretName = os.environ['secretName']

    response = secretsmanager.get_secret_value(SecretId=secretName)
    secret = json.loads(response['SecretString'])
    api_key = secret['alphavantage0']

    base_url = 'https://www.alphavantage.co/query?function=LISTING_STATUS'
    CSV_URL = f'{base_url}&apikey={api_key}'

    results = []
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.DictReader(decoded_content.splitlines(), delimiter=',')
        results = list(cr)

    for row in results:
        process_row(row, sfn, stateMachineArn)

    # TODO: Update the daily count for alpha vantage


def process_row(row, sfn, stateMachineArn):
    symbol = row['symbol']
    name = row['name']
    asset_type = row['asset_type']
    if should_ignore_row(symbol, name, asset_type):
        print(f'ignoring symbol={symbol}, name={name}, type={asset_type}')
    else:
        print(f'executing for symbol={symbol}')
        response = sfn.start_execution(stateMachineArn=stateMachineArn,
                                       input=json.dumps({'ticker': symbol}))
        print(response)


def should_ignore_row(symbol, name, asset_type):
    return asset_type == 'ETF' \
        or '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name
