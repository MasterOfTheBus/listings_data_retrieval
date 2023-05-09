import boto3
import os
from datetime import date, time, datetime, timedelta, timezone


def handler(event, context):
    ddb = boto3.client('dynamodb')
    table = os.environ['table']
    num_keys = os.environ['num_keys']
    key_limit = os.environ['key_limit']
    key_table = os.environ['key_table']

    next_symbol = event['symbol']

    response = ddb.get_item(TableName=table, Key={
        'Type': {'S': 'daily'}
    })
    day = response['Item']['Day']['S']
    count = response['Item']['Count']['N']

    response = ddb.get_item(TableName=key_table, Key={
        'Type': {'N': '0'}
    })
    key = int(response['Item']['value']['S'])

    result = determine_wait(count=count, key=key, day=day,
                            key_limit=key_limit, num_keys=num_keys)

    if result['reset_db'] is True:
        reset_db(table=table, ddb=ddb)

    result['symbol'] = next_symbol
    return result


def determine_wait(count, key, day, key_limit, num_keys):
    daily_limit = key_limit * num_keys
    return_value = {'wait': False, 'key': key, 'reset_db': False}
    if key_limit * key == count:
        return_value['key'] = key + 1
    if count >= daily_limit:
        return_value['key'] = 1
        if current_day_before_or_equals_saved_date(day):
            next_day = calc_next_day_timestamp(get_current_day_utc())
            return_value['wait'] = True
            return_value['next_day'] = next_day
        else:
            return_value['reset_db'] = True

    return return_value


def calc_next_day_timestamp(current_date):
    noon_time_local = time(hour=12)
    next_day = current_date + timedelta(days=1)
    next_datetime = datetime.combine(date=next_day, time=noon_time_local,
                                     tzinfo=timezone.utc)
    return next_datetime.isoformat(timespec='seconds').replace("+00:00", "Z")


def current_day_before_or_equals_saved_date(saved_date_str):
    saved_date = date.fromisoformat(saved_date_str)
    return saved_date >= get_current_day_utc()


def get_current_day_utc():
    today = datetime.today()
    return date(year=today.year, month=today.month, day=today.day)


def reset_db(table, ddb):
    today = get_current_day_utc().isoformat()
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
