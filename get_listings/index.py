import boto3
import requests
import os

s3 = boto3.client('s3')
bucket = os.environ['bucket']
api_key = os.environ['apiKey']
base_url = 'https://www.alphavantage.co/query?function=LISTING_STATUS'

CSV_URL = f'{base_url}&apikey={api_key}'


def handler(event, context):

    with requests.Session() as s:
        download = s.get(CSV_URL)
        if download.status_code % 200 > 100:
            return {
                "success": False,
                "reason": "Failed Request"
            }

        s3.put_object(Bucket=bucket, Key='listings.csv', Body=download.content)

        return {
            "success": True
        }
