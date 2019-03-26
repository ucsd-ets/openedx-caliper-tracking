import logging

from track.backends import BaseBackend

from openedx_caliper_tracking.base_transformer import base_transformer, page_view_transformer
from openedx_caliper_tracking.caliper_config import EVENT_MAPPING


logger = logging.getLogger('tracking')


class CaliperProcessor(BaseBackend):
    def __call__(self, event):
        try:
            caliper_event = base_transformer(event)
            related_function = EVENT_MAPPING[event.get('event_type')]
            return related_function(event, caliper_event)
        except KeyError as ex:
            logger.exception("Missing transformer method implementation for %s" % event.get('event_type'))
        except Exception as ex:
            logger.exception(ex.args)

    def send(self, event):
        if not event['event_type'].startswith('/'):
            logger.info(self.__call__(event))
        else:
            logger.info(page_view_transformer(event))
