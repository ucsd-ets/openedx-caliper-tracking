"""
Contains the test cases for openedx_caliper_tracking
application logs delivery to Kafka.
"""
import json

import mock
from django.conf import settings
from django.test import TestCase, override_settings
from kafka.errors import KafkaError
from openedx_caliper_tracking.processor import CaliperProcessor
from openedx_caliper_tracking.tasks import _host_not_found
from openedx_caliper_tracking.tests import TEST_DIR_PATH


class CaliperKafkaTestCase(TestCase):

    def setUp(self):
        input_file = '{}/current/{}'.format(
            TEST_DIR_PATH,
            'book.json'
        )
        with open(input_file) as current:
            self.event = json.loads(current.read())

    @mock.patch(
        'openedx_caliper_tracking.tasks.KafkaProducer',
        autospec=True
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        },
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': True}
    )
    def test_caliper_event_is_delivered_to_kafka_without_error(self, producer_mock):
        """
        Test that  caliper event is delivered with all required settings given.
        """
        CaliperProcessor().__call__(self.event)
        self.assertTrue(producer_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.KafkaProducer',
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        },
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': True}
    )
    def test_caliper_event_delivery_retries_if_kafka_error_occurs(self, producer_mock, send_email_mock):
        """
        Test that in case of kafka error, task retires as per max retries given in the settings.
        Test that delivery failure email report is sent if retries don't come fruitful.
        """
        producer_mock.side_effect = KafkaError
        CaliperProcessor().__call__(self.event)
        self.assertEqual(producer_mock.call_count, settings.CALIPER_KAFKA_SETTINGS.get('MAXIMUM_RETRIES') + 1)
        self.assertTrue(producer_mock.called)
        self.assertTrue(send_email_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.KafkaProducer',
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        },
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': True}
    )
    def test_caliper_event_delivery_failure_email_sent_if_host_not_found(self, producer_mock, send_email_mock):
        """
        Test that in case of host not found error delivery failure report email is sent.
        """
        producer_mock.side_effect = _host_not_found(KafkaError.__class__.__name__, {}, {})
        CaliperProcessor().__call__(self.event)
        self.assertTrue(producer_mock.called)
        self.assertTrue(send_email_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        return_value=0,
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.KafkaProducer',
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        },
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': True}
    )
    def test_caliper_event_delivery_failure_email_not_sent_if_host_not_found(self, producer_mock, send_email_mock):
        """
        Test delivery failure report email failure in case of host not found.
        """
        producer_mock.side_effect = _host_not_found(KafkaError.__class__.__name__, {}, {})
        CaliperProcessor().__call__(self.event)
        self.assertTrue(producer_mock.called)
        self.assertTrue(send_email_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.deliver_caliper_event_to_kafka'
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        },
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': False}
    )
    def test_caliper_event_is_not_delivered_if_flag_is_disable(self, delivery_mock):
        """
        Test events should not be delivered if feature flag ENABLE_KAFKA_FOR_CALIPER is disable.
        """
        CaliperProcessor().__call__(self.event)
        self.assertFalse(delivery_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.deliver_caliper_event_to_kafka'
    )
    @override_settings(
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': True}
    )
    def test_caliper_event_is_not_delivered_if_flag_is_enable_but_settings_not_given(self, delivery_mock):
        """
        Test events should not be delivered if feature flag ENABLE_KAFKA_FOR_CALIPER is disable
        but CALIPER_KAFKA_SETTINGS are not given.
        """
        if hasattr(settings, 'CALIPER_KAFKA_SETTINGS'):
            del settings.CALIPER_KAFKA_SETTINGS

        CaliperProcessor().__call__(self.event)
        self.assertFalse(delivery_mock.called)
