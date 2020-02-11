"""
Transformers for all course discovery events.
"""


def edx_course_discovery_search_initiated(current_event, caliper_event):
    """
    The server emits this event when user clicks on Discover New tab in
    the LMS to view all the available courses.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_event.update({
        'type': 'Event',
        'action': 'Searched',
        'object': {
            'id': current_event['referer'],
            'type': 'WebPage',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context']['course_id']
    })

    return caliper_event


def edx_course_discovery_search_results_displayed(current_event, caliper_event):
    """
    The server emits this event when user clicks on Discover New tab in
    the LMS to view all the available courses.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_event.update({
        'type': 'ViewEvent',
        'action': 'Viewed',
        'object': {
            'id': current_event['referer'],
            'type': 'WebPage',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context']['course_id']
    })

    return caliper_event
