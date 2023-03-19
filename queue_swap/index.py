import boto3
import os

exec_timeout = 900  # timeout is 15 minutes or 900 seconds


def handler(event, context):
    sqs = boto3.client('sqs')
    ddb = boto3.client('dynamodb')
    table = os.environ['table']
    wait_time_str = int(os.environ['waitTime'])
    wait_time = int(wait_time_str) if wait_time_str is not None else 20
    buffer_str = os.environ['buffer']
    buffer = int(buffer_str) if buffer_str is not None else 5

    queue_info = get_queue_info(sqs, ddb, table)

    if queue_info['send_q_count'] == queue_info['recv_q_count']:
        return {'queue_empty': True}
    send_queue_url = queue_info['send_q_url']
    recv_queue_url = queue_info['recv_q_url']
    send_queue_name = queue_info['send_q']
    recv_queue_name = queue_info['recv_q']
    count = queue_info['recv_q_count']

    iterations = calc_iterations(count, exec_timeout,
                                 wait_time, buffer)

    print(f'Received total of {count} messages from {recv_queue_name}.'
          f' Sending {iterations} to {send_queue_name}')

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
    send_q = get_single_queue_info(sqs, ddb, table, 'send_queue')
    recv_q = get_single_queue_info(sqs, ddb, table, 'receive_queue')

    queue_info = {
        'send_q': send_q['name'], 'recv_q': recv_q['name'],
        'send_q_url': send_q['url'], 'recv_q_url': recv_q['url'],
        'send_q_count': send_q['count'], 'recv_q_count': recv_q['count']
    }

    return queue_info


def get_single_queue_info(sqs, ddb, table, type):
    item = ddb.get_item(TableName=table, Key={
        'queue': {'S': type}})
    q_name = item['Item']['name']['S']

    response = sqs.get_queue_url(QueueName=q_name)
    q_url = response['QueueUrl']

    q_attr = sqs.get_queue_attributes(
        QueueUrl=q_url, AttributeNames=['ApproximateNumberOfMessages'])

    count = int(q_attr['Attributes']['ApproximateNumberOfMessages'])
    return {
        'name': q_name, 'url': q_url, 'count': count
    }


def update_queue_assignment(ddb, send_q_name, recv_q_name, table):
    ddb_update(ddb, table, 'send_queue', recv_q_name)
    ddb_update(ddb, table, 'receive_queue', send_q_name)


def ddb_update(ddb, table, key, value):
    ddb.update_item(TableName=table, Key={'queue': {'S': key}},
                    ExpressionAttributeNames={
                        '#N': 'name'
                    },
                    ExpressionAttributeValues={
                        ':name': {'S': value},
                    },
                    UpdateExpression='SET #N=:name')
