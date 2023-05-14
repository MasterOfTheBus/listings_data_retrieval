import boto3
import os
import json


def handler(event, context):
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    bucket = os.environ['bucket']
    topic = os.environ['topic']
    num_parallel = os.environ['num_parallel']

    rows_data = []
    if event is not None and 'listings' in event:
        rows_data = event['listings']
    else:
        response = s3.get_object(Bucket=bucket, Key='listings.csv')
        byte_data = response['Body'].read()
        str_data = byte_data.decode('utf-8')
        rows_data = str_data.split('\n')

    symbols = get_list_of_symbols(rows_data)
    remaining_symbols = send_events(sns, symbols, topic, num_parallel)

    return {'listings': remaining_symbols,
            'queue_empty': len(remaining_symbols) == 0}


def read_file_data(response):
    byte_data = response['Body'].read()
    str_data = byte_data.decode('utf-8')
    return str_data.split('\n')


def get_list_of_symbols(rows_data):
    symbols = []
    for row_str in rows_data[1:]:
        # Ignore empty row
        if row_str == '':
            continue
        row = row_str.split(',')
        symbol = row[0]
        name = row[1]
        asset_type = row[3]  # assetType
        if should_ignore_row(symbol, name, asset_type):
            print(f'ignoring symbol={symbol}, name={name}, type={asset_type}')
        else:
            print(f'queuing symbol={symbol}')
            symbols.append(symbol)

    return symbols


def send_events(sns, symbols, topic, num_parallel):
    iterations = min(len(symbols), num_parallel)
    for i in range(iterations):
        print(f'Sending event for {symbols[i]}')
        sns.publish(TopicArn=topic, Message=json.dumps({'symbol': symbols[i]}))

    return symbols[num_parallel:]


def should_ignore_row(symbol, name, asset_type):
    return asset_type == 'ETF' \
        or '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name
