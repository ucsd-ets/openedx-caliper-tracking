"""
Contains the test cases for openedx_caliper_tracking
application logs delivery to Kafka.
"""
import json

import mock
from django.test import TestCase, override_settings
from kafka.errors import KafkaError

from openedx_caliper_tracking.processor import CaliperProcessor
from openedx_caliper_tracking.tasks import (host_not_found, deliver_caliper_event_to_kafka,
                                            sent_kafka_failure_email, send_system_recovery_email,
                                            HOST_ERROR_CACHE_KEY, EMAIL_DELIVERY_CACHE_KEY)
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
        'openedx_caliper_tracking.processor.deliver_caliper_event_to_kafka.delay',
        autospec=True,
    )
    @override_settings(
        LMS_ROOT_URL='https://localhost:18000',
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        },
        FEATURES={'ENABLE_KAFKA_FOR_CALIPER': True}
    )
    def test_caliper_event_is_delivered_to_kafka_without_error_using_celery(self, delivery_mock):
        """
        Test that  caliper event is delivered with
        all required settings given using celery.
        """
        CaliperProcessor().__call__(self.event)
        self.assertTrue(delivery_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.sent_kafka_failure_email.delay',
        autospec=True
    )
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
    )
    def test_deliver_caliper_event_to_kafka_without_using_celery_without_error(self, producer_mock,
                                                                               sent_email_mock, logger_mock):
        """
        Test that  caliper event is delivered with all
        required settings given without using celery and any error.
        """
        deliver_caliper_event_to_kafka({}, 'book')
        self.assertTrue(producer_mock.called)
        self.assertFalse(sent_email_mock.called)
        self.assertFalse(logger_mock.error.called)
        logger_mock.info.assert_called_with('Logs Delivered Successfully: Event (book) has been successfully'
                                            ' sent to kafka (http://localhost:9092).')

    @mock.patch(
        'openedx_caliper_tracking.tasks.cache.get',
        autospec=True,
        side_effect=lambda CACHE_KEY: {HOST_ERROR_CACHE_KEY: False, EMAIL_DELIVERY_CACHE_KEY: True}[CACHE_KEY]
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.send_system_recovery_email.delay',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.sent_kafka_failure_email.delay',
        autospec=True
    )
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
    )
    def test_deliver_caliper_event_to_kafka_without_celery_without_error_with_system_recovered(self, producer_mock,
                                                                                               sent_email_mock,
                                                                                               logger_mock,
                                                                                               recovery_mail_mock,
                                                                                               cache_mock):
        """
        Test that  caliper event is delivered with all required
        settings given without using celery and any error.
        """
        deliver_caliper_event_to_kafka({}, 'book')
        self.assertTrue(producer_mock.called)
        self.assertFalse(sent_email_mock.called)
        self.assertFalse(logger_mock.error.called)
        self.assertTrue(recovery_mail_mock.called)
        self.assertTrue(cache_mock.called)
        logger_mock.info.assert_called_with('Logs Delivered Successfully: Event (book) has been successfully'
                                            ' sent to kafka (http://localhost:9092).')

    @mock.patch(
        'openedx_caliper_tracking.tasks.cache.get',
        autospec=True,
        return_value=True
    )
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
    )
    def test_deliver_caliper_event_to_kafka_without_celery_with_host_not_found_error_already_occurred(self,
                                                                                                      producer_mock,
                                                                                                      cache_mock):
        deliver_caliper_event_to_kafka({}, 'book')
        self.assertTrue(producer_mock.called)
        cache_mock.assert_called_with(HOST_ERROR_CACHE_KEY)

    @mock.patch(
        'openedx_caliper_tracking.tasks.deliver_caliper_event_to_kafka.retry',
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.sent_kafka_failure_email.delay',
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.KafkaProducer',
        autospec=True,
        side_effect=KafkaError
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 3
        }
    )
    def test_deliver_caliper_event_to_kafka_without_celery_with_error_with_retry(self, producer_mock, sent_email_mock,
                                                                                 logger_mock, retry_mock):
        """
        Test that caliper event is not delivered to kafka
        when error is occurred and retry code is executed.
        """
        deliver_caliper_event_to_kafka({}, 'book')
        self.assertTrue(producer_mock.called)
        self.assertFalse(sent_email_mock.called)
        logger_mock.error.assert_called_with('Logs Delivery Failed: Could not deliver event (book) to kafka'
                                             ' (http://localhost:9092) because of KafkaError.')
        self.assertTrue(retry_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.sent_kafka_failure_email.delay',
        autospec=True
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.KafkaProducer',
        autospec=True,
        side_effect=KafkaError
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'END_POINT': 'http://localhost:9092',
            'TOPIC_NAME': 'dummy topic',
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
            'MAXIMUM_RETRIES': 0
        }
    )
    def test_deliver_caliper_event_to_kafka_without_celery_with_error_without_retry(self, producer_mock,
                                                                                    sent_email_mock, logger_mock):
        """
        Test that caliper event is not delivered to kafka when error is occurred
        and at last retry failure email task is called.
        """
        deliver_caliper_event_to_kafka({}, 'book')
        self.assertTrue(producer_mock.called)
        self.assertTrue(sent_email_mock.called)
        logger_mock.error.assert_called_with('Logs Delivery Failed: Could not deliver event (book) to kafka'
                                             ' (http://localhost:9092) because of KafkaError.')

    @mock.patch(
        'openedx_caliper_tracking.tasks.sent_kafka_failure_email.delay',
        autospec=True,
    )
    def test_host_not_found_error(self, sent_email_mock):
        host_not_found(mock.MagicMock(), self.event, 'book')
        self.assertTrue(sent_email_mock.called)

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        autospec=True,
        return_value=True
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
        }
    )
    def test_sent_kafka_failure_email_with_success(self, send_notification_mock, logger_mock):
        """
        Test that kafka failure email is sent successfully.
        """
        sent_kafka_failure_email('Dummy Error')
        self.assertTrue(send_notification_mock.called)
        logger_mock.info.assert_called_with('Email Sent Successfully: Events delivery failure report'
                                            ' sent to dummy@example.com.')

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.cache.get',
        autospec=True,
        return_value=True
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
        }
    )
    def test_sent_kafka_failure_email_with_email_already_sent(self, cache_mock, logger_mock):
        """
        Test that kafka failure email is not sent if it is already sent.
        """
        sent_kafka_failure_email('Dummy Error')
        self.assertTrue(cache_mock.called)
        logger_mock.info.assert_called_with('Email Already Sent: Events delivery failure report'
                                            ' has been already sent to dummy@example.com.')

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        autospec=True,
        return_value=False
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
        }
    )
    def test_sent_kafka_failure_email_with_failure(self, send_notification_mock, logger_mock):
        """
        Test that if sending kafka failure email is failed an error message is logged.
        """
        sent_kafka_failure_email('Dummy Error')
        self.assertTrue(send_notification_mock.called)
        logger_mock.error.assert_called_with('Email Sending Failed: Could not send events delivery'
                                             ' failure report to dummy@example.com.')

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        autospec=True,
        return_value=True
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
        }
    )
    def test_send_system_recovery_email_with_success(self, send_notification_mock, logger_mock):
        send_system_recovery_email()
        self.assertTrue(send_notification_mock.called)
        logger_mock.info.assert_called_with('Email Sent Successfully: Events delivery success report sent to '
                                            'dummy@example.com.')

    @mock.patch(
        'openedx_caliper_tracking.tasks.LOGGER',
        autospec=True,
    )
    @mock.patch(
        'openedx_caliper_tracking.tasks.send_notification',
        autospec=True,
        return_value=False
    )
    @override_settings(
        CALIPER_KAFKA_SETTINGS={
            'ERROR_REPORT_EMAIL': 'dummy@example.com',
        }
    )
    def test_send_system_recovery_email_with_failure(self, send_notification_mock, logger_mock):
        """
        Test that if sending kafka failure email is failed an error message is logged.
        """
        send_system_recovery_email()
        self.assertTrue(send_notification_mock.called)
        logger_mock.error.assert_called_with('Email Sending Failed: Could not send events delivery success report to '
                                             'dummy@example.com.')
