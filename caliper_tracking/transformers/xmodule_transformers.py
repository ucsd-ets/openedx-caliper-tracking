"""
Transformer for all xmodule events
"""

from django.conf import settings


def xmodule_partitions_assigned_user_to_partition(current_event, caliper_event):
    """
    When a student views a module that is set up to test different child modules,
    the server checks the user_api_usercoursetag table for the student assignment
    to the relevant partition, and to a group for that partition.

    The partition ID is the user_api_usercoursetag.key.

    The group ID is the user_api_usercoursetag.value.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'member': {
            'id': caliper_event['actor']['id'],
            'name': current_event['username'],
            'type': 'Person',
            'extensions': {
                'user_id': caliper_event['extensions']['extra_fields'].pop('user_id'),
            }
        },
        'organization': {
            'extensions': current_event['event'],
            'id': current_event['referer'],
            'type': 'Group'
        },
        'type': 'Membership'
    }

    caliper_event.update({
        'type': 'Event',
        'action': 'Linked',
        'object': caliper_object,
    })

    caliper_event['actor'].update({
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication',
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags']
    })

    return caliper_event
