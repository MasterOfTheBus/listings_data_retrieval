import boto3
import os
from datetime import date

ddb = boto3.client('dynamodb')
table = os.environ['table']
daily_limit = os.environ['daily_limit']


def handler(event, context):

    response = ddb.get_item(TableName=table, Key={
        'Type': {'S': 'daily'}
    })
    day = response['Item']['Day']['S']
    count = response['Item']['Count']['N']

    if count >= daily_limit:
        count_date = date.fromisoformat(day)
        print(count_date)
        if count_date >= date.today():
            return {'wait': True}
        else:
            print('reset count to 0')

    return {'wait': False}
