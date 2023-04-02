import boto3
import os
from datetime import date, time, datetime, timedelta


def handler(event, context):
    ddb = boto3.client('dynamodb')
    table = os.environ['table']
    daily_limit = os.environ['daily_limit']

    next_symbol = event['symbol']

    response = ddb.get_item(TableName=table, Key={
        'Type': {'S': 'daily'}
    })
    day = response['Item']['Day']['S']
    count = response['Item']['Count']['N']

    if count >= daily_limit:
        if current_day_before_or_equals_saved_date(day):
            next_day = calc_wait_until_next_day(date.today())
            return {'wait': True, 'symbol': next_symbol, 'next_day': next_day}
        else:
            today = date.today().isoformat()
            ddb.update_item(TableName=table, Key={'Type': {'S': 'daily'}},
                            ExpressionAttributeNames={
                                '#D': 'Day',
                                '#C': 'Count'
                            },
                            ExpressionAttributeValues={
                                ':day': {'S': today},
                                ':count': {'N': '0'}
                            },
                            UpdateExpression='SET #D=:day, #C=:count')
            print(f'reset count to 0, day to {today}')

    return {'wait': False, 'symbol': next_symbol}


def calc_wait_until_next_day(current_date):
    noon_time_local = time(hour=12)
    next_day = current_date + timedelta(days=1)
    return datetime.combine(date=next_day, time=noon_time_local)


def current_day_before_or_equals_saved_date(saved_date_str):
    saved_date = date.fromisoformat(saved_date_str)
    return saved_date >= date.today()
