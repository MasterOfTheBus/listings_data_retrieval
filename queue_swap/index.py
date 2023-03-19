import boto3
import os

exec_timeout = 900  # timeout is 15 minutes or 900 seconds


def handler(event, context):
    sqs = boto3.client('sqs')
    ddb = boto3.client('dynamodb')
    table = os.environ['table']
    wait_time = os.environ['waitTime']
    buffer = os.environ['buffer']

    queue_info = get_queue_info(sqs, ddb, table)

    if queue_info['send_q_count'] == queue_info['recv_q_count']:
        return {'queue_empty': True}
    send_queue_url = queue_info['send_q_url']
    recv_queue_url = queue_info['recv_q_url']
    send_queue_name = queue_info['send_q']
    recv_queue_name = queue_info['recv_q']
    count = queue_info['recv_q_count']

    print(f'Receiving {count} messages from {recv_queue_url} '
          f'to send to {send_queue_url}')

    iterations = calc_iterations(count, exec_timeout, int(wait_time), buffer)
    for i in range(iterations):
        # Use long polling to get messages
        response = sqs.receive_message(QueueUrl=recv_queue_url,
                                       AttributeNames=['SentTimestamp'],
                                       WaitTimeSeconds=wait_time)
        messages = response['Messages']
        if (len(messages) == 0):
            continue

        message = response['Messages'][0]
        print('Deleting: ' + message['Body'])
        sqs.delete_message(QueueUrl=recv_queue_url,
                           ReceiptHandle=message['ReceiptHandle'])

        print('Resending: ' + message['Body'])
        sqs.send_message(QueueUrl=send_queue_url, MessageBody=message['Body'])

    rem_count = count - iterations
    if rem_count <= 0:
        update_queue_assignment(ddb, send_queue_name, recv_queue_name, table)

    return {
        "queue_empty": False,
        "rem_count": rem_count
    }


def calc_iterations(count, exec_time, poll_time, buffer):
    # Subtract 5 for some buffer
    max_iterations = (exec_time / poll_time) - buffer
    return min(count, max_iterations)


def get_queue_info(sqs, ddb, table):
    send_q_item = ddb.get_item(TableName=table, Key={
        'queue': {'S': 'send_queue'}})
    send_q_name = send_q_item['Item']['name']['S']
    recv_q_item = ddb.get_item(TableName=table, Key={
        'queue': {'S': 'receive_queue'}})
    recv_q_name = recv_q_item['Item']['name']['S']

    response = sqs.get_queue_url(QueueName=send_q_name)
    send_q_url = response['QueueUrl']
    response = sqs.get_queue_url(QueueName=recv_q_name)
    recv_q_url = response['QueueUrl']

    # Read Messages that are about to expire and write them back to the queue
    send_q_attr = sqs.get_queue_attributes(
        QueueUrl=send_q_url, AttributeNames=['ApproximateNumberOfMessages'])
    recv_q_attr = sqs.get_queue_attributes(
        QueueUrl=recv_q_url, AttributeNames=['ApproximateNumberOfMessages'])

    send_count = int(send_q_attr['Attributes']['ApproximateNumberOfMessages'])
    recv_count = int(recv_q_attr['Attributes']['ApproximateNumberOfMessages'])

    queue_info = {
        'send_q': send_q_name, 'recv_q': recv_q_name,
        'send_q_url': send_q_url, 'recv_q_url': recv_q_url,
        'send_q_count': send_count, 'recv_q_count': recv_count
    }

    return queue_info


def update_queue_assignment(ddb, send_q_name, recv_q_name, table):
    ddb.update_item(TableName=table, Key={'queue': {'S': 'send_queue'}},
                    AttributeUpdates={
        'name': {'Value': {'S': recv_q_name}}, 'Action': 'PUT'
                    })
    ddb.update_item(TableName=table, Key={'queue': {'S': 'receive_queue'}},
                    AttributeUpdates={
        'name': {'Value': {'S': send_q_name}}, 'Action': 'PUT'
                    })
