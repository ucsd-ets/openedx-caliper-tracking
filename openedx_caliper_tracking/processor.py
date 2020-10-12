import logging
import json
import requests

from django.conf import settings
from requests.exceptions import ConnectionError

from openedx_caliper_tracking.base_transformer import base_transformer, page_view_transformer
from openedx_caliper_tracking.caliper_config import EVENT_MAPPING
from openedx_caliper_tracking.loggers import get_caliper_logger
from openedx_caliper_tracking.tasks import deliver_caliper_event_to_kafka

try:
    # if app is running in edx-platfrom get BaseBackend from edx codebase
    from track.backends import BaseBackend
except (NameError, ImportError):
    # if app is running locally for testing use Testing Backend
    from openedx_caliper_tracking.tests.testing_backend import BaseBackend


LOGGER = logging.getLogger(__name__)
TRACKING_LOGGER = logging.getLogger('tracking')
CALIPER_LOGGER = get_caliper_logger('caliper', 'local2')


def log_success(event_id, status_code):
    """
    This function logs the successful delivery of the caliper event
    to the external API

    @params:
    event_id: (str) UUID of the caliper event
    status_code: (int) HTTP status code of the repsonse from the API
    """
    LOGGER.info('Success {}: Caliper event delivery successful for event id: {} to endpoint: {}'.format(
        status_code,
        event_id,
        settings.CALIPER_DELIVERY_ENDPOINT
    ))


def log_failure(event_id, status_code):
    """
    This function logs the failed delivery of the caliper event
    to the external API

    @params:
    event_id: (str) UUID of the caliper event
    status_code: (int) HTTP status code of the repsonse from the API
    """
    LOGGER.error('Failure {}: Caliper event delivery failed for event id: {} to endpoint: {}'.format(
        status_code,
        event_id,
        settings.CALIPER_DELIVERY_ENDPOINT
    ))


def deliver_caliper_event(caliperized_event, event_type):
    """
    Delivers the caliperized event to the external API endpoint.

    @params
    caliperized_event: (dict) dict containing the entire event after caliperization
    event_type: (str) the type of the event being fired
    """
    try:
        response = requests.post(
            settings.CALIPER_DELIVERY_ENDPOINT,
            headers={
                'Authorization': 'Bearer {}'.format(
                    settings.CALIPER_DELIVERY_AUTH_TOKEN),
                'Content-Type': 'application/vnd.kafka.json.v2+json',
            },
            json={
                "records": [
                    {
                        "key": event_type,
                        "value": caliperized_event
                    }
                ]
            }
        )

        if response.status_code == 200:
            log_success(caliperized_event.get('id'), response.status_code)
        else:
            log_failure(caliperized_event.get('id'), response.status_code)
    except ConnectionError:
        log_failure(caliperized_event.get('id'), 500)


class CaliperProcessor(BaseBackend):
    """
    Is responsible for capturing, transforming and sending all the event tracking logs
    generated by Open edX platform.

    This transformer is used in the commong.djangoapps.track django app as a replacement
    for the default tracking backend.

    It is also used as an addition to the event tracking pipeline in the
    event_tracking app by Open edX.
    """

    def __call__(self, event):
        """
        Handles the transformation and delivery of an event.

        Delivers the event to the caliper log file as well as
        delivers it to an external API if configured to do so.

        @params:
        event: raw event from edX event tracking pipeline
        """
        try:
            caliper_event = base_transformer(event)
            related_function = EVENT_MAPPING[event.get('event_type')]
            transformed_event = related_function(event, caliper_event)

            CALIPER_LOGGER.info(json.dumps(transformed_event))

            if (settings.FEATURES.get('ENABLE_CALIPER_EVENTS_DELIVERY')
                and hasattr(settings, 'CALIPER_DELIVERY_ENDPOINT')
                    and hasattr(settings, 'CALIPER_DELIVERY_AUTH_TOKEN')):
                deliver_caliper_event(transformed_event, event.get('event_type'))

            if settings.FEATURES.get('ENABLE_KAFKA_FOR_CALIPER') and hasattr(settings, 'CALIPER_KAFKA_SETTINGS'):
                deliver_caliper_event_to_kafka.delay(transformed_event, event.get('event_type'))

            return event
        except KeyError:
            LOGGER.warning('Missing transformer method implementation for {}'.format(
                event.get('event_type')))
        except Exception as ex:
            LOGGER.exception(ex.args)

    def send(self, event):
        """
        Implements the abstract send method in track.backends.BaseBackend

        @params:
        event: (dict) raw event from edX event tracking pipeline:
        """
        if not event['event_type'].startswith('/'):
            TRACKING_LOGGER.info(self.__call__(event))
        else:
            TRACKING_LOGGER.info(json.dumps(event))
            CALIPER_LOGGER.info(page_view_transformer(event))
