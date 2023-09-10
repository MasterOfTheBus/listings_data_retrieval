import unittest
import boto3
from moto import mock_dynamodb
from index import update_db


@mock_dynamodb
class TestCreateRecords(unittest.TestCase):

    def test_save_symbols_to_ddb(self):
        table = 'symbols'
        records = [{'symbol': 'A', 'next': 'B'}]

        ddb = boto3.resource('dynamodb', region_name='us-east-1')
        ddb.create_table(TableName=table,
                         AttributeDefinitons={},
                         KeySchema={})

        update_db(ddb, table, records)
        # Shouldn't throw error


if __name__ == '__main__':
    unittest.main()
