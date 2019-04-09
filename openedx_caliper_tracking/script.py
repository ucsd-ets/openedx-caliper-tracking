import os
import json
import requests
from datetime import datetime

from loggers import get_test_logger, get_formatted_log
from settings import CALIPER_AUTH

CALIPER_TESTS_API_URL = CALIPER_AUTH.get('CALIPER_TESTS_API_URL')
CALIPER_TESTS_API_TOKEN = CALIPER_AUTH.get('CALIPER_TESTS_API_TOKEN')


TEST_DIR_PATH = 'tests'
TESTS_LOG_FILE = 'caliper_tests.log'


logger = get_test_logger('caliper_tests', TESTS_LOG_FILE)


test_files = [
    file for file in os.listdir(
        '{}/expected/'.format(TEST_DIR_PATH)
    ) if file.endswith(".json")
]
for file in test_files:
    test_json = json.load(
        open('{}/expected/{}'.format(TEST_DIR_PATH, file), 'r'))
    if not '@context' in test_json:
        continue
    TEST_ENVELOP = {
        "sensor": "https://example.edu/sensors/1",
        "sendTime": str(datetime.now())[:-3] + 'Z',
        "dataVersion": "http://purl.imsglobal.org/ctx/caliper/v1p1",
        "data": [test_json]
    }
    BEARER_TOKEN = 'Bearer {}'.format(CALIPER_TESTS_API_TOKEN)
    headers = {
        'Authorization': BEARER_TOKEN,
        'Content-Type': "application/json",
    }
    response = requests.request('POST',
                                CALIPER_TESTS_API_URL,
                                data=json.dumps(TEST_ENVELOP),
                                headers=headers
                                )
    if response.status_code == requests.codes.ok:
        logger.info(
            get_formatted_log(
                'OK', file, test_json['extensions']['extra_fields']['event_type'], response.status_code)
        )
    else:
        logger.error(
            get_formatted_log(
                'ERROR', file, test_json['extensions']['extra_fields']['event_type'], response.status_code)
        )


