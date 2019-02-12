"""
Transformers for all course related events.
"""

from django.conf import settings
from django.core.urlresolvers import reverse


def edx_course_enrollment_activated(current_event, caliper_event):
    """
    When a student enrolls in a course, the server emits an
    edx.course.enrollment.activated event.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Activated',
        'object': {
            'id': caliper_event['referrer']['id'],
            'type': 'Membership',
            'extensions': {
                'mode': current_event['event']['mode'],
                'course_id': current_event['context']['course_id'],
                'user_id': caliper_event['extensions']['extra_fields'].pop(
                    'user_id')
            }
        },
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].update({
        'event_source': current_event['event_source'],
        'ip': current_event['ip'],

    })
    return caliper_event


def edx_course_enrollment_deactivated(current_event, caliper_event):
    """
    The server emits an enrollment.deactivated event when the student's
    enrollment is cancelled.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """

    course_id = current_event['context']['course_id']

    course_link = '{lms_url}{profile_link}'.format(
        lms_url=settings.LMS_ROOT_URL,
        profile_link=str(reverse(
            'about_course',
            kwargs={'course_id': course_id}
        ))
    )

    caliper_object = {
        'id': course_link,
        'type': 'Membership',
        'extensions': {
            'course_id': course_id,
            'mode': current_event['event']['mode']
        }
    }

    caliper_event.update({
        'object': caliper_object,
        'type': 'Event',
        'action': 'Deactivated',
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_course_enrollment_mode_changed(current_event, caliper_event):
    """
    The server emits an enrollment.mode_changed event when the student's
    enrollment mode is changed.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': {
            'id': current_event['referer'],
            'type': 'Membership',
            'extensions': {
                'course_id': current_event['context']['course_id'],
                'org_id': current_event['context']['org_id'],
                'mode': current_event['event']['mode'],
            }
        },
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip']
    })

    return caliper_event


def edx_course_enrollment_upgrade_clicked(current_event, caliper_event):
    """
    The server emits an enrollment.upgrade_clicked event when the student
    clicks on Upgrade Enrollment Button.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """

    caliper_object = {
        'id': current_event['page'],
        'type': 'WebPage',
    }

    caliper_event.update({
        'type': 'NavigationEvent',
        'action': 'NavigatedTo',
        'object': caliper_object,

    })

    caliper_event['extensions']['extra_fields'].update({
        'event': current_event['event'],
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    return caliper_event


def edx_course_enrollment_upgrade_succeeded(current_event, caliper_event):
    """
    This event is generated when the user is successfully upgraded, from honor
    to verified or so, in a course.

    :param current_event: default log
    :param caliper_event: log containing both basic and default attribute
    :return: final created log
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': {
            'id': caliper_event['referrer']['id'],
            'type': 'Membership',
            'extensions': {
                'mode': current_event['event']['mode'],
                'course_id': current_event['context']['course_id'],
                'user_id': caliper_event['extensions']['extra_fields']
                    .pop('user_id'),
                'org_id': caliper_event['extensions']['extra_fields']
                    .pop('org_id')
            }
        },
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].update({
        'event_source': current_event['event_source'],
        'ip': current_event['ip'],

    })
    return caliper_event
