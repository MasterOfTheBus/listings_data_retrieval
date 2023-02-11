import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')
events = boto3.client('events')


def handler(event, context):
    bucket = os.environ['bucket']
    # Default will be 5
    minute_limit = os.environ['minute_limit']
    # Should be divisible by minute_limit. Default will be 500
    day_limit = os.environ['day_limit']

    response = s3.get_object(Bucket=bucket, Key='listings.csv')
    byte_data = response['Body'].read()
    str_data = byte_data.decode('utf-8')
    rows_data = str_data.split('\n')

    map_symbol_to_date(row_data=rows_data, daily_limit=day_limit,
                       minute_limit=minute_limit, handler=create_schedule)

    return {
        "success": True
    }


def map_symbol_to_date(row_data, daily_limit, minute_limit, mapping_handler):
    day_time = datetime.today() + timedelta(days=1)  # Start with the next day
    symbols_per_day = daily_limit / minute_limit
    day_count = 0
    name_set = set()

    # Ignore the header row
    for row_str in row_data[1:]:
        row = row_str.split(',')
        symbol = row[0]
        name = row[1]
        type = row[3]
        if should_ignore_row(symbol, name, type):
            # print(f'ignoring symbol={symbol}, name={name}')
            continue

        unhyphenated_name = name.split(' - ')[0]
        if unhyphenated_name in name_set:
            # print(f'ignoring symbol={symbol}, name={name}')
            continue
        name_set.add(unhyphenated_name)

        mapping_handler(symbol=symbol, day_time=day_time)

        # Increment the minute and day count
        day_count = day_count + 1
        if day_count == symbols_per_day:
            day_count = 0
            day_time = day_time + timedelta(days=1)  # Next day
        else:
            day_time = day_time + timedelta(minutes=1)  # Next minute


def should_ignore_row(symbol, name, type):
    return type == 'ETF' \
        or '-' in symbol \
        or '- Units' in name \
        or '- Warrants' in name \
        or 'Acquisition' in name \
        or 'TEST' in name


def create_schedule(symbol, day_time):
    events.put_rule(Name=symbol,
                    ScheduleExpression=f'cron({datetime_to_cron(day_time)})',
                    State='ENABLED')


def datetime_to_cron(day_time):
    # Minutes Hours DayOfMonth Month DayOfWeek Year
    return day_time.strftime('%M %H %d %m ? %Y')
