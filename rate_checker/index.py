import boto3
import os

ddb = boto3.client('dynamodb')
table = os.environ['table']


def handler(event, context):

    #     Daily: day, count
    # Get Daily from DDB
    # If count > 500
    # 	return response to wait
    # else return response to continue

    response = ddb.get_item(TableName=table, Key={
        'Type': {'S': 'daily'}
    })

    print(response)

    return {
        "success": True
    }
