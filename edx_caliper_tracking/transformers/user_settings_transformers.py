"""
Transformers for all the user setting events
"""
import json


def edx_user_settings_viewed(current_event, caliper_event):
    """
    Event occur when you go to your Account Settings Page.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    object_extensions = json.loads(current_event['event'])

    caliper_object = {
        'id': current_event['referer'],
        'type': 'WebPage',
        'extensions': object_extensions
    }

    caliper_event.update({
        'type': 'ViewEvent',
        'action': 'Viewed',
        'object': caliper_object
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['extensions']['extra_fields'].pop('user_id')

    return caliper_event


def edx_user_settings_changed(current_event, caliper_event):
    """
    Event occurs when a user changes anything in his/her account settings page.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    object_extensions = current_event['event']

    caliper_object = {
        'id': caliper_event['actor']['id'],
        'type': 'Person',
        'extensions': object_extensions
    }

    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': caliper_object
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    return caliper_event


def edx_bi_course_upgrade_sidebarupsell_displayed(current_event, caliper_event):
    """
    Browser emits this event when sidebar for upgrading course is displayed on course page.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    object_extensions = json.loads(current_event['event'])

    caliper_object = {
        'id': current_event['referer'],
        'type': 'Frame',
        'extensions': object_extensions
    }

    caliper_event.update({
        'type': 'ViewEvent',
        'action': 'Viewed',
        'object': caliper_object
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    return caliper_event
