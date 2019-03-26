import logging
import json

from track.backends import BaseBackend

from openedx_caliper_tracking.base_transformer import base_transformer, page_view_transformer
from openedx_caliper_tracking.caliper_config import EVENT_MAPPING
from openedx_caliper_tracking.loggers import get_caliper_logger

logger = logging.getLogger('tracking')
caliper_logger = get_caliper_logger('caliper', '/dev/caliper.log')


class CaliperProcessor(BaseBackend):
    def __call__(self, event):
        try:
            caliper_event = base_transformer(event)
            related_function = EVENT_MAPPING[event.get('event_type')]
            caliper_logger.info(json.dumps(related_function(event, caliper_event)))
            return event
        except KeyError as ex:
            logger.exception("Missing transformer method implementation for {0}".format(event.get('event_type')))
        except Exception as ex:
            logger.exception(ex.args)

    def send(self, event):
        if not event['event_type'].startswith('/'):
            logger.info(self.__call__(event))
        else:
            logger.info(json.dumps(event))
            caliper_logger.info(page_view_transformer(event))
