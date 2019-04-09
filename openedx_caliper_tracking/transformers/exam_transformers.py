"""
Transformers for all exam related events.
"""
from openedx_caliper_tracking.utils import convert_datetime


def edx_special_exam_timed_attempt_created(current_event, caliper_event):
    """
    The server emits this event when a learner chooses to take a special exam.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': current_event['referer'],
            'type': 'Attempt',
            'name': current_event['event'].pop('exam_name'),
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_special_exam_timed_attempt_submitted(current_event, caliper_event):
    """
    The server emits this event when a learner completes a proctored exam
    and submits it for grading and review.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'AssessmentEvent',
        'action': 'Submitted',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
            'name': current_event['event'].pop('exam_name'),
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context'].get('course_user_tags'),
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_special_exam_timed_attempt_started(current_event, caliper_event):
    """
    The server emits this event when a learner begins taking a proctored exam.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'AssessmentEvent',
        'action': 'Started',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
            'name': current_event['event'].pop('exam_name'),
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_special_exam_timed_attempt_deleted(current_event, caliper_event):
    """
    The server emits this event when a course team or edX platform administrator
    removes an exam attempt record for an individual learner.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Deleted',
        'object': {
            'id': current_event['referer'],
            'type': 'Attempt',
        }
    })
    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    if current_event['event'].get('attempt_started_at'):
        caliper_event['object']['startedAtTime'] = convert_datetime(
            current_event['event'].pop(
                'attempt_started_at'
            ))

    if current_event['event'].get('attempt_completed_at'):
        caliper_event['object']['endedAtTime'] = convert_datetime(
            current_event['event'].pop(
                'attempt_completed_at'
            ))

    caliper_event['object'].update({
        'extensions': current_event['event']
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_special_exam_practice_attempt_created(current_event, caliper_event):
    """
    The server emits this event when a learner chooses to take a special exam.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': current_event['referer'],
            'type': 'Attempt',
            'name': current_event['event'].pop('exam_name'),
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event


def edx_special_exam_proctored_created(current_event, caliper_event):
    """
    The server emits this event when a course instructor creates Proctored Exam.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
        }
    })

    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    caliper_event['object'].update({
        'extensions': current_event['event']
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_special_exam_practice_created(current_event, caliper_event):
    """
    The server emits this event when a course instructor creates Practice Exam.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
        }
    })

    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    caliper_event['object'].update({
        'extensions': current_event['event']
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_special_exam_practice_updated(current_event, caliper_event):
    """
    The server emits this event when a instructor changes exam type.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
        }
    })

    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    caliper_event['object'].update({
        'extensions': current_event['event']
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_special_exam_timed_updated(current_event, caliper_event):
    """
    The server emits this event when a instructor changes the time limit for timed exams.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
        }
    })

    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    caliper_event['object'].update({
        'extensions': current_event['event']
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_special_exam_proctored_updated(current_event, caliper_event):
    """
    The server emits this event when a instructor changes exam type.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Modified',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
        }
    })

    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    caliper_event['object'].update({
        'extensions': current_event['event']
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_special_exam_timed_created(current_event, caliper_event):
    """
    The server emits this event when a course instructor creates Timed Exam.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'Event',
        'action': 'Created',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
        }
    })

    if current_event['event'].get('exam_name'):
        caliper_event['object']['name'] = current_event['event'].pop('exam_name')

    caliper_event['object'].update({
        'extensions': current_event['event']
    })

    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })

    caliper_event['referrer']['type'] = 'WebPage'

    return caliper_event


def edx_special_exam_time_attempt_ready_to_submit(current_event, caliper_event):
    """
    The server emits this event when a learner has completed a proctored exam
    and is prompted to submit the exam.

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
            'name': current_event['event'].pop('exam_name'),
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    return caliper_event
