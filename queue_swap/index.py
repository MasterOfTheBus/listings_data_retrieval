import boto3
import os
from datetime import datetime


def handler(event, context):
    sqs = boto3.client('sqs')
    queue = os.environ['queue']
    batch = int(os.environ['batch'])
    delta = int(os.environ['delta'])

    response = sqs.get_queue_url(QueueName=queue)
    queue_url = response['QueueUrl']

    # Read Messages that are about to expire and write them back to the queue
    attributes = sqs.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])

    count = int(attributes['Attributes']['ApproximateNumberOfMessages'])
    if count == 0:
        return {
            "queue_empty": True
        }

    def receive_messages():
        return sqs.receive_message(QueueUrl=queue_url,
                                   AttributeNames=['SentTimestamp'],
                                   MaxNumberOfMessages=batch)

    def send_and_delete_messages(entries):
        to_send = [{'Id': ind, 'MessageBody': x['Body']} for ind, x
                   in enumerate(entries)]
        sqs.send_message_batch(QueueUrl=queue_url, Entries=to_send)
        to_delete = [{'Id': ind, 'ReceiptHandle': x['ReceiptHandle']}
                     for ind, x in enumerate(entries)]
        sqs.delete_message_batch(QueueUrl=queue_url, Entries=to_delete)

    iterations = 1
    if count > batch:
        iterations = count // batch
        if not count % batch == 0:
            iterations = iterations + 1

    for i in range(iterations):
        should_continue = handle_batch(receive_messages,
                                       send_and_delete_messages,
                                       delta)
        if not should_continue:
            break

    return {
        "queue_empty": False
    }


def handle_batch(receive, send_and_delete, delta):
    should_continue = True
    messages = receive()

    to_requeue = []
    for message in messages:
        timestamp = int(message['Attributes']['SentTimestamp'])
        sent_date = datetime.fromtimestamp(timestamp / 1000)
        today = datetime.today()
        days_delta = today - sent_date
        if days_delta.days >= delta:
            to_requeue.append(message)
        else:
            should_continue = False

    if len(to_requeue) == 0:
        return False

    send_and_delete(to_requeue)

    return should_continue
