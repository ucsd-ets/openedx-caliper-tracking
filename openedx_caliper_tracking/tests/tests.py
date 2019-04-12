"""
This module contains the test cases for openedx_caliper_tracking application
"""

import json
import mock
import os

from django.conf import settings
from django.test import TestCase, override_settings

from openedx_caliper_tracking.base_transformer import base_transformer
from openedx_caliper_tracking.caliper_config import EVENT_MAPPING
from openedx_caliper_tracking.processor import CaliperProcessor

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
    def test_caliper_transformers(self, *args):
        """
        Tests whether all the caliper transformers are working as expected
        """
        test_files = [test for test in os.listdir(
            '{}/current/'.format(TEST_DIR_PATH)) if test.endswith(".json")]

        for current_file in test_files:
            input_file = '{}/current/{}'.format(
                TEST_DIR_PATH,
                current_file
            )
            output_file = '{}/expected/{}'.format(
                TEST_DIR_PATH,
                current_file
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


class CaliperDeliveryTestCase(TestCase):
    """
    Test that determines that caliper app is properly delivering the data
    to an external API
    """

    @mock.patch(
        'openedx_caliper_tracking.processor.deliver_caliper_event'
    )
    @override_settings()
    def test_event_is_not_called_without_settings(self, delivery_mock):
        """
        If the settings CALIPER_DELIVER_ENDPOINT and CALIPER_DELIVERY_AUTH_TOKEN are
        not present then the API call shouldn't fire
        """
        del settings.CALIPER_DELIVERY_ENDPOINT
        del settings.CALIPER_DELIVERY_AUTH_TOKEN
        input_file = '{}/current/{}'.format(
            TEST_DIR_PATH,
            'book.json'
        )
        with open(input_file) as current:
            event = json.loads(current.read())

            CaliperProcessor().__call__(event)

        delivery_mock.assert_not_called()

    @mock.patch(
        'openedx_caliper_tracking.processor.deliver_caliper_event'
    )
    @override_settings(
        CALIPER_DELIVERY_ENDPOINT='http://localhost:3000',
        CALIPER_DELIVERY_AUTH_TOKEN='test_auth_token',
    )
    def test_event_is_called_with_settings(self, delivery_mock):
        """
        If the settings are present then the delivery method
        should be called
        """
        input_file = '{}/current/{}'.format(
            TEST_DIR_PATH,
            'book.json'
        )
        with open(input_file) as current:
            event = json.loads(current.read())

            CaliperProcessor().__call__(event)

        delivery_mock.assert_called()
