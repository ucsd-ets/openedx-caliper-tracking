"""
Contains the test cases for openedx_caliper_tracking
application logs delivery to Rest API.
"""
import json

import mock
from django.conf import settings
from django.test import TestCase, override_settings

from openedx_caliper_tracking.processor import CaliperProcessor
from openedx_caliper_tracking.tests import TEST_DIR_PATH


class CaliperDeliveryTestCase(TestCase):
    """
    Test that determines that caliper app is properly delivering the data
    to an external API
    """

    def setUp(self):
        input_file = '{}/current/{}'.format(
            TEST_DIR_PATH,
            'book.json'
        )
        with open(input_file) as current:
            self.event = json.loads(current.read())

    @mock.patch(
        'openedx_caliper_tracking.processor.deliver_caliper_event'
    )
    def test_event_is_not_called_without_settings(self, delivery_mock):
        """
        Test that API call shouldn't fire if the following settings

            ENABLE_CALIPER_EVENTS_DELIVERY,
            CALIPER_DELIVERY_ENDPOINT,
            CALIPER_DELIVERY_AUTH_TOKEN

        are not given.
        """
        if settings.FEATURES.get('ENABLE_CALIPER_EVENTS_DELIVERY'):
            settings.FEATURES.pop('ENABLE_CALIPER_EVENTS_DELIVERY')

        if hasattr(settings, 'CALIPER_DELIVERY_ENDPOINT'):
            del settings.CALIPER_DELIVERY_ENDPOINT

        if hasattr(settings, 'CALIPER_DELIVERY_AUTH_TOKEN'):
            del settings.CALIPER_DELIVERY_AUTH_TOKEN

        CaliperProcessor().__call__(self.event)
        self.assertFalse(delivery_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.processor.deliver_caliper_event'
    )
    @override_settings(
        CALIPER_DELIVERY_ENDPOINT='http://localhost:3000',
        CALIPER_DELIVERY_AUTH_TOKEN='test_auth_token',
        FEATURES={'ENABLE_CALIPER_EVENTS_DELIVERY': False}
    )
    def test_event_is_not_called_with_unset_delivery_flag(self, delivery_mock):
        """
        Test that API call shouldn't fire if the feature flag ENABLE_CALIPER_EVENTS_DELIVERY is not set.
        """
        CaliperProcessor().__call__(self.event)
        self.assertFalse(delivery_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.processor.deliver_caliper_event',
        autospec=True
    )
    @override_settings(
        CALIPER_DELIVERY_ENDPOINT='http://localhost:3000',
        CALIPER_DELIVERY_AUTH_TOKEN='test_auth_token',
        FEATURES={'ENABLE_CALIPER_EVENTS_DELIVERY': True}
    )
    def test_event_is_called_with_settings(self, delivery_mock):
        """
        Test that  caliper event is delivered with all required settings given.
        """
        CaliperProcessor().__call__(self.event)
        self.assertTrue(delivery_mock.called)
