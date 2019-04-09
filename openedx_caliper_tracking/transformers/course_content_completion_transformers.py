"""
Transformers for all Course Content Completion Events
"""
import json


def edx_done_toggled(current_event, caliper_event):
    """
    Both the browser and the server emit the edx.done.toggled event when the control added by the
    Completion XBlock is toggled. The event_source field indicates whether the event was emitted by
    the client or the server.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'action': 'Used',
        'type': 'ToolUseEvent',
        'object': {
            'id': current_event['referer'],
            'type': 'SoftwareApplication',
        }
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    if current_event.get('event_source') == 'server':
        caliper_event['extensions']['extra_fields'].pop('session')
        caliper_event['object']['extensions'] = current_event['event']
    else:
        caliper_event['object'].update({
            'extensions': json.loads(current_event['event'])
        })

    return caliper_event
