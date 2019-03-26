"""
Base module containing generic caliper transformer class
"""
import uuid
import json

from openedx_caliper_tracking import utils

CALIPER_EVENT_CONTEXT = 'http://purl.imsglobal.org/ctx/caliper/v1p1'


def base_transformer(event):
    """Transforms event into caliper format
    @param event: unprocessed event dict
    """
    caliper_event = {}

    _add_generic_fields(event, caliper_event)
    _add_actor_info(event, caliper_event)
    _add_referrer(event, caliper_event)
    _add_extensions(event, caliper_event)

    return caliper_event


def page_view_transformer(event):
    """Transforms page view events into caliper format

    @param event: non-caliperized event dict
    @return : caliperized event dict
    """

    caliper_event = base_transformer(event)

    caliper_event['actor']['type'] = 'Person'
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['type'] = 'NavigationEvent'
    caliper_event['action'] = 'NavigatedTo'
    caliper_event['object'] = {
        'id': event.get('referer'),
        'type': 'WebPage',
        'extensions': event.get('event')
    }
    caliper_event['extensions']['extra_fields'].update(event.get('context'))
    caliper_event_str = json.dumps(caliper_event)
    return caliper_event_str


def _add_generic_fields(event, caliper_event):
    """
    Adds all of the generic fields to the caliper_event object.

    @param event: unprocessed event dict
    @param caliper_event: caliper event dict
    """
    caliper_event.update({
        '@context': CALIPER_EVENT_CONTEXT,
        'id': uuid.uuid4().urn,
        'eventTime': utils.convert_datetime(event.get('time'))
    })


def _add_actor_info(event, caliper_event):
    """
    Adds all generic information related to `actor`

    @param event: unprocessed event dict
    @param caliper_event: caliper event dict
    """
    caliper_event['actor'] = {}
    user_profile_link = utils.get_user_link_from_username(event.get('username'))
    caliper_event['actor'].update({
        'id': user_profile_link,
    })


def _add_extensions(event, caliper_event):
    """
    A map of additional attributes not defined by the model MAY be
    specified for a more concise representation of the Event.

    @param event: unprocessed event dict
    @param caliper_event: caliper event dict
    """
    caliper_event['extensions'] = {}
    caliper_event['extensions']['extra_fields'] = {
        'agent': event.get('agent'),
        'event_type': event.get('event_type'),
        'event_source': event.get('event_source'),
        'host': event.get('host'),
        'org_id': event['context'].get('org_id'),
        'path': event['context'].get('path'),
        'session': event.get('session'),
        'user_id': event['context'].get('user_id'),
        'accept_language': event.get('accept_language'),
        'page': event.get('page'),
    }


def _add_referrer(event, caliper_event):
    """
    Adds information of an Entity that represents the referring context.

    @param event: unprocessed event dict
    @param caliper_event: caliper event dict
    """
    caliper_event['referrer'] = {
        'id': event.get('referer')
    }
