"""
Transformers for segment events
"""

import json

from django.conf import settings


def edx_bi_email_sent(current_event, caliper_event):
    """
    This event is generated when an email is sent to user to notify
    them about something e.g. when there is a first comment on the user's
    post in a discussion (although this notification requires
    "enable_forum_notifications" to be set to true in site configuration).


    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Posted',
        'object': {
            'id': current_event['referer'],
            'type': 'Message',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'] = {
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication'
    }

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_user_tags': current_event['context'].get('course_user_tags')
    })

    return caliper_event


def edx_bi_schedule_suppressed(current_event, caliper_event):
    """
    This event is generated when an scheduled email to the about upgrade
    deadline is suppressed by the system. These emails are suppressed based
    on the configurations for schedules.

    To create such schedules:
    - create schedule config from admin panel with holdback value > 1.
      1 means always suppress while zero means never suppress.
    - Goto LMS admin panel
    - Create waffle switch `student.courseenrollment_admin` and waffle
      flag `create_schedules_for_course`
    - create a self paced course
    - enroll in course

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Skipped',
        'object': {
            'id': current_event['referer'],
            'type': 'Message',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'] = {
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication'
    }

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
    })

    return caliper_event



def edx_bi_user_account_events(current_event, caliper_event):
    """
    This event is generated when a user is authenticated using either the login
    form or any oauth provider.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'SessionEvent',
        'action': 'LoggedIn',
        'object': {
            'id': settings.LMS_ROOT_URL,
            'type': 'Session',
            'extensions': current_event['event']
        }
    })

    if current_event.get('name') == 'edx.bi.user.account.linked':
        caliper_event['action'] = 'Linked'
        caliper_event['type'] = 'Event'

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event.get('username')
    })

    caliper_event['referrer']['id'] = current_event['referer']

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
    })

    return caliper_event


def edx_bi_user_account_registered(current_event, caliper_event):
    """
    This event is generated when a new user is registered.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': caliper_event['actor']['id'],
            'type': 'Person',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event.get('username')
    })

    caliper_event['referrer']['id'] = current_event['referer']

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
    })

    return caliper_event


def edx_bi_user_certificate_generate(current_event, caliper_event):
    """
    This event is generated when a user is granted a certificate.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    current_path =current_event['context'].get('path')
    if current_path:
        object_id = '{}{}'.format(settings.LMS_ROOT_URL, current_path)
    else:
        object_id = current_event.get('referer')

    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': object_id,
            'type': 'Document',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'].update({
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication',
    })

    caliper_event['referrer']['id'] = current_event['referer']

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
        'course_user_tags': current_event['context'].get('course_user_tags'),
    })

    return caliper_event


def edx_bi_user_org_email_events(current_event, caliper_event):
    """
    These events are generated when a user is opted in our out for
    a course organization emails.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    action = 'Subscribed' if current_event['name'] == 'edx.bi.user.org_email.opted_in' else 'Unsubscribed'

    caliper_event.update({
        'type': 'Event',
        'action': action,
        'object': {
            'id': current_event['referer'],
            'type': 'CourseOffering',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event.get('username')
    })

    caliper_event['referrer']['id'] = current_event['referer']

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
    })

    return caliper_event


def edx_bi_verify_submitted(current_event, caliper_event):
    """
    These events are generated when a user submits photos for verification.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_event.update({
        'type': 'Event',
        'action': 'Submitted',
        'object': {
            'id': current_event['referer'],
            'type': 'ImageObject',
            'extensions': current_event['event']
        }
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event.get('username')
    })

    caliper_event['referrer']['id'] = current_event['referer']

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
    })

    return caliper_event
