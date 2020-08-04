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
from openedx_caliper_tracking.exceptions import InvalidConfigurationsError
from openedx_caliper_tracking.kafka_utils import get_kafka_producer_configurations
from openedx_caliper_tracking.loggers import get_caliper_logger

LOGGER = logging.getLogger(__name__)
CALIPER_DELIVERY_FAILURE_LOGGER = get_caliper_logger(
    'caliper_delivery_failure', 'local3'
)

EMAIL_DELIVERY_CACHE_KEY = 'IS_KAFKA_DELIVERY_FAILURE_EMAIL_SENT'
HOST_ERROR_CACHE_KEY = 'HOST_NOT_FOUND_ERROR'

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
REPORT_EMAIL_VALIDITY_PERIOD = 86400  # in ms. Equals to one day.

MAXIMUM_RETRIES = getattr(settings, 'CALIPER_KAFKA_SETTINGS', {}).get('MAXIMUM_RETRIES', 3)


@task(bind=True, max_retries=MAXIMUM_RETRIES)
def deliver_caliper_event_to_kafka(self, transformed_event, event_type):
    """
    Deliver caliper event to kafka.

    Retries for the given number of max_tries in case of any error else
    sends an error report to the specified email address.
    """
    KAFKA_SETTINGS = settings.CALIPER_KAFKA_SETTINGS

    bootstrap_servers = KAFKA_SETTINGS['PRODUCER_CONFIG']['bootstrap_servers']
    topic_name = KAFKA_SETTINGS['TOPIC_NAME']

    try:
        LOGGER.info('Attempt # {} of sending event: {} to kafka ({}) is in progress.'.format(
                    self.request_stack().get('retries'), event_type, bootstrap_servers))

        try:
            producer_configrations = get_kafka_producer_configurations()
            producer = KafkaProducer(
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                **producer_configrations
            )

        # Invalid/unsupported arguments are provided
        except (TypeError, AttributeError) as ex:
            LOGGER.exception(
                'Invalid configurations are provided for KafkaProducer: %s', str(ex)
            )
            raise InvalidConfigurationsError('Invalid Configurations are provided')

        # Most probably a certificate file was not found.
        except IOError as ex:
            LOGGER.exception(
                'Configured Certificate is not found: %s', str(ex)
            )
            raise InvalidConfigurationsError('Invalid Configurations are provided')

        producer.send(topic_name, transformed_event).add_errback(host_not_found,
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
            event_type, bootstrap_servers))

    except KafkaError as error:
        LOGGER.error(('Logs Delivery Failed: Could not deliver event ({}) to kafka ({}) because'
                      ' of {}.').format(event_type, bootstrap_servers, error.__class__.__name__))

        if self.request_stack().get('retries') == KAFKA_SETTINGS['MAXIMUM_RETRIES']:
            CALIPER_DELIVERY_FAILURE_LOGGER.info(json.dumps(transformed_event))
            sent_kafka_failure_email.delay(error.__class__.__name__)
            return

        self.retry(exc=error, countdown=int(
            random.uniform(2, 4) ** self.request.retries))

    except InvalidConfigurationsError as ex:
        # No need to retry the task if there is some configurations issue.
        LOGGER.error(('Logs Delivery Failed: Could not deliver event ({}) to kafka ({}) due'
                      ' to the error: {}').format(
                          event_type,
                          bootstrap_servers,
                          str(ex)
        ))

        sent_kafka_failure_email.delay(ex.__class__.__name__)


def host_not_found(error, event, event_type):
    """
    Callback method.

    It would be called in case of "Host Not Found" error.
    """
    HOST_NOT_FOUND_ERROR = 'Host Not Found'
    LOGGER.error('Logs Delivery Failed: Could not deliver event ({}) to kafka ({}) because of {}.'.format(
        event_type,
        settings.CALIPER_KAFKA_SETTINGS['PRODUCER_CONFIG']['bootstrap_servers'],
        HOST_NOT_FOUND_ERROR
    ))
    cache.set(HOST_ERROR_CACHE_KEY, True)
    sent_kafka_failure_email.delay(HOST_NOT_FOUND_ERROR)


@task(bind=True)
def sent_kafka_failure_email(self, error):
    """
    Send error report to specified email address.
    """
    reporting_emails = settings.CALIPER_KAFKA_SETTINGS.get('ERROR_REPORT_EMAILS')
    if not reporting_emails:
        return

    if cache.get(EMAIL_DELIVERY_CACHE_KEY):
        LOGGER.info('Email Already Sent: Events delivery failure report has been already sent to {}.'.format(
            reporting_emails))
        return

    data = {
        'name': 'UCSD Support',
        'body': 'Below is the additional information regarding failure:'
                '\nSystem URL = {}'.format(settings.LMS_ROOT_URL),
        'error': error
    }
    subject = 'Failure in logs delivery to Kafka'
    if send_notification(data, subject, DEFAULT_FROM_EMAIL, reporting_emails):
        success_message = 'Email Sent Successfully: Events delivery failure report sent to {}.'.format(
            reporting_emails)
        # after one day if the delivery of events to kafka still fails,
        # email failure  delivery report again.
        cache.set(EMAIL_DELIVERY_CACHE_KEY, True,
                  timeout=REPORT_EMAIL_VALIDITY_PERIOD)
        LOGGER.info(success_message)
    else:
        failure_message = 'Email Sending Failed: Could not send events delivery failure report to {}.'.format(
            reporting_emails)
        LOGGER.error(failure_message)


@task(bind=True)
def send_system_recovery_email(self):
    """
    Send system recovery report to specified email address.
    """
    reporting_emails = settings.CALIPER_KAFKA_SETTINGS.get('ERROR_REPORT_EMAILS')
    if not reporting_emails:
        return

    data = {
        'name': 'UCSD Support',
        'body': 'System has been recovered. Now Caliper logs are being successfully delivered to kafka.'
                '\nSystem URL = {}'.format(settings.LMS_ROOT_URL),
    }
    subject = 'Success in logs delivery to Kafka'
    if send_notification(data, subject, DEFAULT_FROM_EMAIL, reporting_emails):
        success_message = 'Email Sent Successfully: Events delivery success report sent to {}.'.format(
            reporting_emails)
        LOGGER.info(success_message)
    else:
        failure_message = 'Email Sending Failed: Could not send events delivery success report to {}.'.format(
            reporting_emails)
        LOGGER.error(failure_message)
