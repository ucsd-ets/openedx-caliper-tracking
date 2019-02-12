"""
Transformers for all the bookmark events
"""
import json


def edx_bookmark_listed(current_event, caliper_event):
    """
    The server emits this event when a user clicks Bookmarks under
    the Course Tools heading in the LMS to view the list of previously
    bookmarked pages. If the number of bookmarks exceeds the defined
    page length, the browser emits an additional edx.course.bookmark.listed
    event each time the user navigates to a different page of results.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_event.update({
        'type': 'NavigationEvent',
        'action': 'NavigatedTo',
        'object': {
            'id': current_event['referer'],
            'type': 'WebPage',
            'extensions': {
                'course_id': current_event['event'].get('course_id'),
                'page_number': current_event['event'].get('page_number'),
                'bookmarks_count': current_event['event'].get('bookmarks_count'),
                'page_size': current_event['event'].get('page_size'),
                'list_type': current_event['event'].get('list_type'),
            }
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
    })

    return caliper_event


def edx_bookmark_added(current_event, caliper_event):
    """
    The server emits this event when a user removes a bookmark from a page.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update(
        {
            'type': 'AnnotationEvent',
            'action': 'Bookmarked',
            'object': {
                'id': current_event['referer'],
                'type': 'Page',
                'extensions': {
                    'course_id': current_event['event']['course_id'],
                    'bookmark_id': current_event['event']['bookmark_id'],
                    'component_usage_id': current_event['event']['component_usage_id'],
                    'component_type': current_event['event']['component_type']
                }
            }
        }
    )
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'path': current_event['context']['path'],
    })
    return caliper_event


def edx_bookmark_accessed(current_event, caliper_event):
    """
    When bookmarks are accessed.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'action': 'NavigatedTo',
        'type': 'NavigationEvent'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context'].get('course_id'),
        'ip': current_event.get('ip')
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['actor'].update({
        'name': current_event.get('username'),
        'type': 'Person'
    })
    event_info = json.loads(current_event['event'])
    caliper_event['object'] = {
        'id': current_event.get('referer'),
        'type': 'WebPage',
        'extensions': event_info
    }
    return caliper_event


def edx_bookmark_removed(current_event, caliper_event):
    """
    When a bookmark is removed/deleted.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'action': 'Deleted',
        'type': 'Event'
    })
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['actor'].update({
        'name': current_event.get('username'),
        'type': 'Person'
    })
    caliper_event['object'] = {
        'id':  current_event.get('referer'),
        'type': 'BookmarkAnnotation',
        'extensions': current_event['event']
    }
    return caliper_event
