"""
This module contains the test cases for openedx_caliper_tracking application
"""

import mock
import json
import os

from django.test import TestCase

from openedx_caliper_tracking.base_transformer import base_transformer
from openedx_caliper_tracking.caliper_config import EVENT_MAPPING

TEST_DIR_PATH = os.path.dirname(os.path.abspath(__file__))


class CaliperTransformationTestCase(TestCase):
    """
    Data driven test case that tests all transformers for expected output
    The test case compares the files in the current/ directory
    and compares them with their corresponding files in the expected/ directory
    """

    maxDiff = None

    @mock.patch(
        'openedx_caliper_tracking.utils.get_username_from_user_id',
        return_value='honor',
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.utils.get_team_url_from_team_id',
        return_value=(
                "http://localhost:18000/courses/course-v1:edX+DemoX+Demo_Course/teams/"
                "#teams/Topic1ID/check-3429fc5983a84c8c8366a4477b03d91c"
        ),
        autospec=True
    )
    def test_caliper_transformers(self, user_mock, team_mock):
        test_files = [file for file in os.listdir(
            '{}/current/'.format(TEST_DIR_PATH)) if file.endswith(".json")]

        for file in test_files:
            input_file = '{}/current/{}'.format(
                TEST_DIR_PATH,
                file
            )
            output_file = '{}/expected/{}'.format(
                TEST_DIR_PATH,
                file
            )

            with open(input_file) as current, open(output_file) as expected:
                event = json.loads(current.read())
                expected_event = json.loads(expected.read())

                expected_event.pop('id')

                caliper_event = base_transformer(event)
                related_function = EVENT_MAPPING[event.get('event_type')]
                caliper_event = related_function(event, caliper_event)

                caliper_event.pop('id')

                self.assertDictEqual(caliper_event, expected_event)
