"""
Contains tasks related to Openedx Caliper Tracking.
"""
import json
import logging
import random

from celery.task import task
from django.conf import settings
from kafka import KafkaProducer
from kafka.errors import KafkaError

from openedx.features.ucsd_features.utils import send_notification

LOGGER = logging.getLogger(__name__)
KAFKA_SETTINGS = settings.CALIPER_KAFKA_SETTINGS
DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
MAXIMUM_RETRIES = KAFKA_SETTINGS.get('MAXIMUM_RETRIES')
ERROR_REPORT_EMAIL = KAFKA_SETTINGS.get('ERROR_REPORT_EMAIL')
KAFKA_END_POINT = KAFKA_SETTINGS.get('END_POINT')
KAFKA_TOPIC_NAME = KAFKA_SETTINGS.get('TOPIC_NAME')


@task(bind=True, max_retries=MAXIMUM_RETRIES)
def deliver_caliper_event_to_kafka(self, transformed_event, event_type):
    """
    Deliver caliper event to kafka.

    Retries for the given number of max_tries in case of any error else
    sends an error report to the specified email address.
    """
    try:
        LOGGER.info('Attempt # {} of sending event: {} to kafka is in progress.'.format(
                    self.request_stack().get('retries'), event_type))

        producer = KafkaProducer(bootstrap_servers=KAFKA_END_POINT,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        producer.send(KAFKA_TOPIC_NAME, transformed_event).add_errback(_host_not_found,
                                                                       event=transformed_event,
                                                                       event_type=event_type)
        producer.flush()
        LOGGER.info('Logs Delivered Successfully: Event ({}) has been successfully sent to kafka.'.format(event_type))

    except KafkaError as error:
        LOGGER.error(('Logs Delivery Failed: Could not deliver event ({}) to kafka because'
                     ' of {}.').format(event_type, error))

        if self.request_stack().get('retries') == MAXIMUM_RETRIES:
            sent_kafka_failure_email.delay(error, transformed_event, event_type)
            return

        self.retry(exc=error, countdown=int(random.uniform(2, 4) ** self.request.retries))


def _host_not_found(error, event, event_type):
    """
    Callback method.

    It would be called in case of "Host Not Found" error.
    """
    LOGGER.error('Logs Delivery Failed: Could not deliver event ({}) to kafka because of {}.'.format(event_type, error))
    sent_kafka_failure_email.delay(error, event, event_type)


@task(bind=True)
def sent_kafka_failure_email(self, error, event, event_type):
    """
    Send error report to specified email address.
    """
    additional_info = {
        'Error': str(error),
        'Event Type': event_type,
        'Event': json.dumps(event, sort_keys=True)
    }
    key = 'logs_not_sent'
    data = {
        'name': 'UCSD Support',
        'body': 'Below is the additional information regarding failure:',
        'additional_info': additional_info
    }
    subject = 'Failure in logs delivery to Kafka'
    if send_notification(key, data, subject, DEFAULT_FROM_EMAIL, [ERROR_REPORT_EMAIL]):
        success_message = 'Email Sent Succesfully: Event ({}) Delivery Failure Report Sent to {}.'.format(
            event_type, ERROR_REPORT_EMAIL)
        LOGGER.info(success_message)
    else:
        failure_message = 'Email Sending Failed: Could not send Event ({}) Delivery Failure Report to {}.'.format(
            event_type, ERROR_REPORT_EMAIL)
        LOGGER.error(failure_message)
