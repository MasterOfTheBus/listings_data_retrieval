import boto3
import os
from datetime import date, time, datetime, timedelta, timezone


def handler(event, context):
    ddb = boto3.client('dynamodb')
    table = os.environ['table']
    daily_limit = os.environ['daily_limit']

    next_symbol = event['symbol']
    listings = event['listings']

    response = ddb.get_item(TableName=table, Key={
        'Type': {'S': 'daily'}
    })
    day = response['Item']['Day']['S']
    count = response['Item']['Count']['N']

    rate_check = check_rate_limit(count=count, daily_limit=daily_limit,
                                  day=day, reset_rate=reset_count,
                                  ddb=ddb, table=table)

    response = {'symbol': next_symbol, 'listings': listings}
    response['wait'] = rate_check['wait']
    if 'next_day' in rate_check:
        response['next_day'] = rate_check['next_day']
    return response


def check_rate_limit(count, daily_limit, day, reset_rate, ddb, table):
    if count >= daily_limit:
        if current_day_before_or_equals_saved_date(day):
            next_day = calc_next_day_timestamp(get_current_day_utc())
            return {'wait': True, 'next_day': next_day}
        else:
            reset_rate(ddb, table)

    return {'wait': False}


def calc_next_day_timestamp(current_date):
    noon_time_local = time(hour=0)
    next_day = current_date + timedelta(days=1)
    next_datetime = datetime.combine(date=next_day, time=noon_time_local,
                                     tzinfo=timezone.utc)
    return next_datetime.isoformat(timespec='seconds').replace("+00:00", "Z")


def current_day_before_or_equals_saved_date(saved_date_str):
    saved_date = date.fromisoformat(saved_date_str)
    return saved_date >= date.today()


def reset_count(ddb, table):
    today = get_current_day_utc.isoformat()
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


def get_current_day_utc():
    today = datetime.today()
    return date(year=today.year, month=today.month, day=today.day)
