"""
Contains tasks related to Openedx Caliper Tracking.
"""
import json
import logging
import random

from celery.task import task
from django.conf import settings
from django.core.cache import cache
from kafka import KafkaProducer
from kafka.errors import KafkaError

from openedx_caliper_tracking.utils import send_notification
from openedx_caliper_tracking.loggers import get_caliper_logger

LOGGER = logging.getLogger(__name__)
CALIPER_DELIVERY_FAILURE_LOGGER = get_caliper_logger('caliper_delivery_failure', 'local3')
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
EMAIL_DELIVERY_CACHE_KEY = 'IS_KAFKA_DELIVERY_FAILURE_EMAIL_SENT'
HOST_ERROR_CACHE_KEY = 'HOST_NOT_FOUND_ERROR'


def _get_kafka_setting(key):
    if hasattr(settings, 'CALIPER_KAFKA_SETTINGS'):
        return settings.CALIPER_KAFKA_SETTINGS.get(key)


@task(bind=True, max_retries=_get_kafka_setting('MAXIMUM_RETRIES'))
def deliver_caliper_event_to_kafka(self, transformed_event, event_type):
    """
    Deliver caliper event to kafka.

    Retries for the given number of max_tries in case of any error else
    sends an error report to the specified email address.
    """
    try:
        LOGGER.info('Attempt # {} of sending event: {} to kafka ({}) is in progress.'.format(
                    self.request_stack().get('retries'), event_type, _get_kafka_setting('END_POINT')))

        producer = KafkaProducer(bootstrap_servers=_get_kafka_setting('END_POINT'),
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(_get_kafka_setting('TOPIC_NAME'), transformed_event).add_errback(host_not_found,
                                                                                       event=transformed_event,
                                                                                       event_type=event_type)
        producer.flush()

        if cache.get(HOST_ERROR_CACHE_KEY):
            cache.set(HOST_ERROR_CACHE_KEY, False)
            return

        if cache.get(EMAIL_DELIVERY_CACHE_KEY):
            send_system_recovery_email.delay()
        cache.set(EMAIL_DELIVERY_CACHE_KEY, False)

        LOGGER.info('Logs Delivered Successfully: Event ({}) has been successfully sent to kafka ({}).'.format(
            event_type, _get_kafka_setting('END_POINT')))

    except KafkaError as error:
        LOGGER.error(('Logs Delivery Failed: Could not deliver event ({}) to kafka ({}) because'
                     ' of {}.').format(event_type, _get_kafka_setting('END_POINT'), error.__class__.__name__))

        if self.request_stack().get('retries') == _get_kafka_setting('MAXIMUM_RETRIES'):
            CALIPER_DELIVERY_FAILURE_LOGGER.info(json.dumps(transformed_event))
            sent_kafka_failure_email.delay(error.__class__.__name__)
            return

        self.retry(exc=error, countdown=int(random.uniform(2, 4) ** self.request.retries))


def host_not_found(error, event, event_type):
    """
    Callback method.

    It would be called in case of "Host Not Found" error.
    """
    HOST_NOT_FOUND_ERROR = 'Host Not Found'
    LOGGER.error('Logs Delivery Failed: Could not deliver event ({}) to kafka ({}) because of {}.'.format(
        event_type, _get_kafka_setting('END_POINT'), HOST_NOT_FOUND_ERROR))
    cache.set(HOST_ERROR_CACHE_KEY, True)
    sent_kafka_failure_email.delay(HOST_NOT_FOUND_ERROR)


@task(bind=True)
def sent_kafka_failure_email(self, error):
    """
    Send error report to specified email address.
    """
    if cache.get(EMAIL_DELIVERY_CACHE_KEY):
        LOGGER.info('Email Already Sent: Events delivery failure report has been already sent to {}.'.format(
            _get_kafka_setting('ERROR_REPORT_EMAIL')))
        return

    data = {
        'name': 'UCSD Support',
        'body': 'Below is the additional information regarding failure:',
        'error': error
    }
    subject = 'Failure in logs delivery to Kafka'
    if send_notification(data, subject, DEFAULT_FROM_EMAIL, [_get_kafka_setting('ERROR_REPORT_EMAIL')]):
        success_message = 'Email Sent Successfully: Events delivery failure report sent to {}.'.format(
            _get_kafka_setting('ERROR_REPORT_EMAIL'))
        # after one day if the delivery of events to kafka still fails,
        # email failure  delivery report again.
        cache.set(EMAIL_DELIVERY_CACHE_KEY, True, timeout=86400)
        LOGGER.info(success_message)
    else:
        failure_message = 'Email Sending Failed: Could not send events delivery failure report to {}.'.format(
            _get_kafka_setting('ERROR_REPORT_EMAIL'))
        LOGGER.error(failure_message)


@task(bind=True)
def send_system_recovery_email(self):
    """
    Send system recovery report to specified email address.
    """
    data = {
        'name': 'UCSD Support',
        'body': 'System has been recovered. Now Caliper logs are being successfully delivered to kafka.',
    }
    subject = 'Success in logs delivery to Kafka'
    if send_notification(data, subject, DEFAULT_FROM_EMAIL, [_get_kafka_setting('ERROR_REPORT_EMAIL')]):
        success_message = 'Email Sent Successfully: Events delivery success report sent to {}.'.format(
            _get_kafka_setting('ERROR_REPORT_EMAIL'))
        LOGGER.info(success_message)
    else:
        failure_message = 'Email Sending Failed: Could not send events delivery success report to {}.'.format(
            _get_kafka_setting('ERROR_REPORT_EMAIL'))
        LOGGER.error(failure_message)
