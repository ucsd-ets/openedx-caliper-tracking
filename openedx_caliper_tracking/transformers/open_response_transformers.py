"""
Transformers for all openassessment events
"""

import json

from openedx_caliper_tracking.utils import convert_datetime


def openassessmentblock_get_submission_for_staff_grading(
        current_event, caliper_event):
    """
    When a course team member retrieves a learner's response for grading in the
    staff assessment step the server emits this event.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'type': 'ViewEvent',
        'action': 'Viewed',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
            'extensions': current_event['event']
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'module': current_event['context']['module'],
        'ip': current_event['ip']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event


def openassessmentblock_create_submission(current_event, caliper_event):
    """
    The server emits this event when a learner submits a response.
    The same event is emitted when a learner submits a
    response for peer assessment or for self assessment.

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
            'extensions': {
                'answer': current_event['event']['answer'],
                'attempt_number': current_event['event']['attempt_number'],
                'created_at': convert_datetime(
                    current_event['event']['created_at']),
                'submission_uuid': current_event['event']['submission_uuid'],
                'submitted_at': convert_datetime(
                    current_event['event']['submitted_at'])
            }
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'module': current_event['context']['module']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event


def openassessmentblock_peer_assess(current_event, caliper_event):
    """
    The server emits this event when a learner submits an assessment of
    peer's response.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    current_event_details = current_event['event']
    event_context_details = current_event['context']

    caliper_object = {
        'dateCreated': convert_datetime(
            current_event_details.pop('scored_at')),
        'extensions': current_event_details,
        'id': current_event['referer'],
        'type': 'Attempt'
    }

    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': event_context_details['asides'],
        'course_user_tags': event_context_details['course_user_tags'],
        'course_id': event_context_details['course_id'],
        'module': event_context_details['module'],
        'ip': current_event['ip']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def openassessment_student_training_assess_example(
        current_event, caliper_event):
    """
    The server emits this event when a learner submits a response.
    The same event is emitted when a learner submits a
    response for peer assessment or for self assessment.

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
            'extensions': {
                'corrections': current_event['event']['corrections'],
                'options_selected': current_event['event']['options_selected'],
                'submission_uuid': current_event['event']['submission_uuid']
            }
        }
    })
    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'module': current_event['context']['module']
    })
    caliper_event['actor'].update({
        'type': 'Person',
        'name': current_event['username']
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event


def openassessmentblock_submit_feedback_on_assessments(
        current_event, caliper_event):
    """
    The server emits openassessmentblock_submit_feedback_on_assessments event
    when learner submit feedback.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.

    """

    module_details = current_event['context']['module']

    caliper_object = {
        'extensions': current_event['event'],
        'id': current_event['referer'],
        'type': 'Message'
    }

    caliper_event.update({
        'action': 'Posted',
        'type': 'MessageEvent',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'display_name': module_details['display_name'],
        'usage_key': module_details['usage_key'],
        'ip': current_event['ip']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def openassessmentblock_save_submission(current_event, caliper_event):
    """
    server emits openassessmentblock.save_submission event when user save
    his response before submitting it.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.

    """
    saved_response = json.loads(current_event['event']['saved_response'])
    module_details = current_event['context']['module']

    caliper_object = {
        'extensions': {
            'saved_response': saved_response
        },
        'id': current_event['referer'],
        'type': 'Assessment'
    }

    caliper_event.update({
        'action': 'Paused',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_id': current_event['context']['course_id'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'display_name': module_details['display_name'],
        'usage_key': module_details['usage_key'],
        'ip': current_event['ip']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def openassessmentblock_get_peer_submission(current_event, caliper_event):
    """
    The server emits openassessmentblock.get_peer_submission event  when
    responses of other course participants are delivered to a learner for
    evaluation.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.

    """

    module_details = current_event['context']['module']

    caliper_object = {
        'extensions': current_event['event'],
        'id': current_event['referer'],
        'type': 'Assessment'
    }

    caliper_event.update({
        'action': 'Viewed',
        'type': 'ViewEvent',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'display_name': module_details['display_name'],
        'usage_key': module_details['usage_key'],
        'ip': current_event['ip']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def openassessmentblock_staff_assess(current_event, caliper_event):
    """
    The server emits this event when a course team member submits an
    assessment of a learner's response.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    current_event_details = current_event['event']
    event_context_details = current_event['context']

    caliper_object = {
        'dateCreated': convert_datetime(current_event_details.pop('scored_at')),
        'extensions': current_event_details,
        'id': current_event['referer'],
        'type': 'Attempt'
    }

    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': event_context_details['asides'],
        'course_user_tags': event_context_details['course_user_tags'],
        'course_id': event_context_details['course_id'],
        'module': event_context_details['module'],
        'ip': current_event['ip']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def openassessmentblock_self_assess(current_event, caliper_event):
    """
    The server emits this event when a learner submits an
    assessment of his own response.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    current_event_details = current_event['event']
    event_context_details = current_event['context']

    caliper_object = {
        'dateCreated': convert_datetime(current_event_details.pop('scored_at')),
        'extensions': current_event_details,
        'id': current_event['referer'],
        'type': 'Attempt'
    }

    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': event_context_details['asides'],
        'course_user_tags': event_context_details['course_user_tags'],
        'course_id': event_context_details['course_id'],
        'module': event_context_details['module'],
        'ip': current_event['ip']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def openassessmentblock_save_files_descriptions(current_event, caliper_event):
    """
    The server emits this event when a description of a learner's response
    file is saved on submission.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_object = {
        'extensions': {
            'saved_response': json.loads(
                current_event['event']['saved_response']
            )
        },
        'id': current_event['referer'],
        'type': 'Document',
        'isPartOf': {
            'id': current_event['referer'],
            'type': 'Assessment'
        }
    }

    caliper_event.update({
        'action': 'Described',
        'type': 'Event',
        'object': caliper_object
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update({
        'asides': current_event['context']['asides'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'ip': current_event['ip'],
        'module': current_event['context']['module'],
        'course_id': current_event['context']['course_id']
    })

    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['extensions']['extra_fields'].pop('session')
    
    return caliper_event
