import boto3
import os


def handler(event, context):
    s3 = boto3.client('s3')
    ddb = boto3.client('dynamodb')
    bucket = os.environ['bucket']
    table = os.environ['table']

    response = s3.get_object(Bucket=bucket, Key='listings.csv')
    byte_data = response['Body'].read()
    str_data = byte_data.decode('utf-8')
    rows_data = str_data.split('\n')

    symbols = get_list_of_symbols(rows_data)
    update_db(ddb, table, symbols)

    return {
        "symbol": symbols[0]['symbol']
    }


def get_list_of_symbols(rows_data):
    symbols = []
    for row_str in rows_data[1:]:
        row = row_str.split(',')
        symbol = row[0]
        name = row[1]
        if should_ignore_row(symbol, name):
            print(f'ignoring symbol={symbol}, name={name}')
        else:
            print(f'queuing symbol={symbol}')
            symbols.append(symbol)

    return create_records(symbols)


def create_records(symbols):
    records = []
    for i in range(len(symbols) - 1):
        records.append({'symbol': symbols[i],
                        'next': symbols[i+1]})
    return records


def update_db(ddb, table, records):
    for record in records:
        ddb.put_item(TableName=table, Key={'Type': {'S': 'daily'}},
                     Item={
                        'symbol': {
                            'S': record['symbol']
                        },
                        'next': {
                            'S': record['next']
                        }
                     })


def should_ignore_row(symbol, name):
    return '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name
