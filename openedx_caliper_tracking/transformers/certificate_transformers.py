"""
Transformers for all the certificate events
"""

from openedx_caliper_tracking.utils import get_certificate_url
from django.conf import settings

import json


def edx_certificate_evidence_visited(current_event, caliper_event):
    """
    When a learner shares her certificates on social network sites such
    as LinkedIn, and the link back to the certificate is followed by some
    visitor to that social network site, the server emits an
    edx.certificate.evidence_visited event.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    user_id = current_event['event'].get('user_id')
    course_id = current_event['event'].get('course_id')

    certificate_uri = get_certificate_url(user_id, course_id)

    object_extensions = current_event['event']

    caliper_event.update({
        'type': 'Event',
        'action': 'Showed',
        'object': {
            'id': certificate_uri,
            'type': 'Document',
            'extensions': object_extensions
        }
    })

    caliper_event['actor'].update({
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'referer': current_event.get('referer'),
        'username': current_event.get('username')
    })

    caliper_event['extensions']['extra_fields'].update(
        current_event['context']
    )

    caliper_event.pop('referrer')

    return caliper_event


def edx_certificate_shared(current_event, caliper_event):
    """
    When a learner shares the URL for her certificate on a social media
    web site, the server emits an edx.certificate.shared event.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    object_extensions = json.loads(current_event['event'])

    caliper_event.update({
        'type': 'Event',
        'action': 'Shared',
        'object': {
            'id': object_extensions['certificate_url'],
            'type': 'Document',
            'extensions': object_extensions
        }
    })

    caliper_event['actor'].update({
        'type': 'Person'
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
    })

    return caliper_event


def edx_certificate_created(current_event, caliper_event):
    """
    When a certificate is generated, a record is created in the
    certificates_generatedcertificate table, triggering an
    edx.certificate.created event.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    user_id = current_event['context'].get('user_id')
    course_id = current_event['context'].get('course_id')

    certificate_uri = get_certificate_url(user_id, course_id)

    object_extensions = current_event['event']

    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': certificate_uri,
            'type': 'Document',
            'extensions': object_extensions
        }
    })

    caliper_event['actor'].update({
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication'
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event.get('ip'),
        'course_id': current_event['context'].get('course_id'),
        'course_user_tags': current_event['context'].get('course_user_tags'),
        'username': current_event.get('username')
    })

    return caliper_event
