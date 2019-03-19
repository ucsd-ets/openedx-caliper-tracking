import os
import json
import requests
from datetime import datetime

from paver.easy import task

from pavelib.utils import loggers
from pavelib.settings import CALIPER_TESTS_API_ADDRESS, CALIPER_TESTS_API_TOKEN

TEST_DIR_PATH = 'tests/'
TESTS_LOG_FILE = 'caliper_tests.log'


logger = loggers.get_test_logger('caliper_tests', TESTS_LOG_FILE)


@task
def test_caliper_compliance():
    test_files = [
        file for file in os.listdir(
            '{}expected/'.format(TEST_DIR_PATH)
        ) if file.endswith(".json")
    ]
    for file in test_files:
        test_json = json.load(
            open('{}expected/{}'.format(TEST_DIR_PATH, file), 'r'))
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
            'authorization': BEARER_TOKEN,
            'content-type': "application/json",
        }
        response = requests.request('POST',
                                    CALIPER_TESTS_API_ADDRESS,
                                    data=json.dumps(TEST_ENVELOP),
                                    headers=headers
                                    )
        if response.status_code == requests.codes.ok:
            logger.info('OK [{}][event_type:{}] Returned status: {}'.format(
                file, test_json['extensions']['extra_fields']['event_type'], response.status_code
            ))
        else:
            logger.error('FAILED [{}][event_type:{}] Returned status: {}'.format(
                file, test_json['extensions']['extra_fields']['event_type'], response.status_code
            ))
