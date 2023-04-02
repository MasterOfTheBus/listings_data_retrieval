import json
from datetime import datetime, timedelta, timezone


def prepare_mock_config():
    # Kind of hacky, setup the config to mock a wait for the next 2 minutes
    next_time = datetime.now(timezone.utc) + timedelta(minutes=2)
    with open('data_retrieval_mock_config_base.json', 'r') as f:
        config = json.load(f)
        (config['MockedResponses']
         ['MockedRateCheckerHappyPath']
         ['1']
         ['Return']
         ['Payload']
         ['next_day']) = \
            next_time.isoformat(timespec='seconds').replace("+00:00", "Z")
        with open('data_retrieval_mock_config.json', 'w') as output_file:
            json.dump(config, output_file)


if __name__ == '__main__':
    prepare_mock_config()
