"""
Transformers for all the problems events
"""
import json
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


def problem_reset(current_event, caliper_event):
    """
    The browser emits problem_reset events when the answer to a
    problem given before is reset; that is, the user selected
    Reset.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_object = {
        'id': current_event['page'],
        'type': 'Assessment'
    }
    caliper_event.update({
        'action': 'Reset',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'event': current_event['event'],
        'ip': current_event['ip']
    })
    return caliper_event


def problem_show(current_event, caliper_event):
    """
    The browser emits problem_show events when the answer to a
    problem is shown; that is, the user selected Show Answer.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    current_event_details = json.loads(current_event['event'])

    caliper_object = {
        'id': current_event['referer'],
        'extensions': {
            'problem': current_event_details['problem']
        },
        'type': 'DigitalResource'
    }
    caliper_event.update({
        'action': 'Viewed',
        'type': 'ViewEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'event': current_event['event'],
        'ip': current_event['ip'],
    })
    return caliper_event


def problem_graded(current_event, caliper_event):
    """
    The browser emits problem_graded events when the answer to a
    problem is submitted; that is, the user selected Submitted.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'extensions': {
            'event': current_event['event']
        },
        'type': 'Attempt'
    }
    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip'],
    })
    return caliper_event


def problem_save(current_event, caliper_event):
    """
    The browser emits problem_save events when the answer to a
    problem is save instead of submitting; that is,
    the user selected Save Answer.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'extensions': {
            'event': current_event['event']
        },
        'type': 'Assessment'
    }
    caliper_event.update({
        'action': 'Paused',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'ip': current_event['ip']
    })
    return caliper_event


def save_problem_success(current_event, caliper_event):
    """
    The server emits save_problem_success events when a problem is saved successfully.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event.update({
        'action': 'Paused',
        'type': 'AssessmentEvent',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
            'extensions': current_event['event']
        }
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update({
        'course_id': current_event['context']['course_id'],
        'asides': current_event['context']['asides'],
        'course_user_tags': current_event['context']['course_user_tags'],
        'module': current_event['context']['module'],
        'ip': current_event['ip']
    })
    return caliper_event


def problem_check(current_event, caliper_event):
    """
    The server emits problem_check events when a problem is successfully checked.
    Both browser interactions and server requests produce problem_check events, so your data package
    can also contain events with an event source of browser.
    Events emitted by the browser contain all of the GET parameters.
    Only events emitted by the server are useful for most purposes.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_event.update({
        'action': 'Submitted',
        'type': 'AssessmentEvent',
        'object': {
            'id': current_event['referer'],
            'type': 'Assessment',
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
            'extensions': {
                'event': current_event['event']
            }
        })

    return caliper_event


def edx_problem_hint_demandhint_displayed(current_event, caliper_event):
    """
    Course teams can design problems to include one or more hints. For problems that include hints,
    the server emits an edx.problem.hint.demandhint_displayed event each time a user requests a
    hint.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Frame'
    }

    caliper_event.update({
        'action': 'Viewed',
        'type': 'ViewEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    return caliper_event


def problem_rescore(current_event, caliper_event):
    """
    The server emits problem_rescore events when a problem is successfully
    rescored.
    In these events, the user who rescored the problem is identified in the
    username and context.user_id fields, and the user who originally submitted
    the response to the problem is identified in the student field.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    if not (current_event.get('referer') or current_event['context'].get('referer')):
        logger.exception(
            'Missing "referer" key in event which is required for "object.id"'
            'in caliper events, therefore returning the original event'
        )
        current_event['id'] = None
        return current_event

    caliper_object = {
        'id': current_event['context'].get('referer'),
        'extensions': current_event['event'],
        'type': 'Attempt'
    }

    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'id': current_event['context'].pop('referer'),
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['context'].pop('username'),
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    return caliper_event


def edx_problem_hint_feedback_displayed(current_event, caliper_event):
    """
    Course teams can design problems to include feedback messages that appear
    after a user submits an answer.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Frame'
    }

    caliper_event.update({
        'action': 'Viewed',
        'type': 'ViewEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].pop('session')
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    return caliper_event


def edx_grades_problem_submitted(current_event, caliper_event):
    """
    Occurs when learner submitted submitted a question of peer assignment.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Assessment'
    }

    caliper_event.update({
        'action': 'Submitted',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    return caliper_event


def edx_grades_problem_state_deleted(current_event, caliper_event):
    """
    When a course team member deletes the state for a learner's problem
    submission, the server emits an edx.grades.problem.state_deleted event.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Assessment'
    }

    caliper_event.update({
        'action': 'Reset',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    return caliper_event


def edx_grades_problem_rescored(current_event, caliper_event):
    """
    Server emits this event when problem re-scoring task is accomplished.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    if not current_event.get('referer'):
        logger.exception(
            'Missing "referer" key in event which is required for "object.id"'
            'in caliper events, therefore returning the original event'
        )
        current_event['id'] = None
        return current_event

    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Attempt'
    }

    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'id': current_event['referer'],
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    return caliper_event


def reset_problem_fail(current_event, caliper_event):
    """
    The server emits reset_problem_fail events when a problem cannot be reset successfully.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_object = {
        'id': current_event['referer'],
        'type': 'Assessment',
        'extensions': current_event['event']
    }
    caliper_event.update({
        'action': 'Reset',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],

    })
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event


def edx_grades_problem_score_overridden(current_event, caliper_event):
    """
    Server emits this event when a user's score for a problem is overridden.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    if not current_event.get('referer'):
        logger.exception(
            'Missing "referer" key in event which is required for "object.id"'
            'in caliper events, therefore returning the original event'
        )
        current_event['id'] = None
        return current_event

    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Attempt'
    }

    caliper_event.update({
        'action': 'Graded',
        'type': 'GradeEvent',
        'object': caliper_object
    })

    caliper_event['referrer'].update({
        'type': 'WebPage'
    })

    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })

    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].update({
        'ip': current_event['ip'],
        'event_source': current_event['event_source'],
        'host': current_event['host'],
        'session': current_event['session'],
        'page': current_event['page'],
    })
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']

    return caliper_event


def reset_problem(current_event, caliper_event):
    """
    The server emits reset_problem events when a problem has been reset
    successfully.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_object = {
        'id': current_event['referer'],
        'type': 'Assessment',
        'extensions': current_event['event']
    }
    caliper_event.update({
        'action': 'Reset',
        'type': 'AssessmentEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].update({
        'event_source': current_event['event_source'],
        'event_type': current_event['event_type'],
        'host': current_event['host'],
        'ip': current_event['ip'],
        'page': current_event['page'],
    })
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event


def showanswer(current_event, caliper_event):
    """
    The server emits showanswer events when the answer to a problem is shown.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    caliper_object = {
        'id': current_event['referer'],
        'extensions': current_event['event'],
        'type': 'Frame'
    }
    caliper_event.update({
        'action': 'Viewed',
        'type': 'ViewEvent',
        'object': caliper_object
    })
    caliper_event['referrer'].update({
        'type': 'WebPage'
    })
    caliper_event['actor'].update({
        'name': current_event['username'],
        'type': 'Person'
    })
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    caliper_event['extensions']['extra_fields'].pop('session')

    return caliper_event


def problem_check_fail(current_event, caliper_event):
    """
    The server emits problem_check_fail events when a problem cannot be
    checked successfully.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """

    # transformer code for this event is same as that of problem_check
    return problem_check(current_event, caliper_event)


def save_problem_fail(current_event, caliper_event):
    """
    The server emits save_problem_fail events when a problem cannot be
    saved successfully.

    :param current_event: default event log generated.
    :param caliper_event: caliper_event log having some basic attributes.
    :return: updated caliper_event.
    """
    caliper_event.update({
        'action': 'Abandoned',
        'type': 'Event',
        'object': {
            'id': current_event['referer'],
            'type': 'AssessmentItem',
            'extensions': current_event['event']
        }
    })
    caliper_event['referrer']['type'] = 'WebPage'
    caliper_event['actor'].update({
        'id': settings.LMS_ROOT_URL,
        'type': 'SoftwareApplication',
    })
    caliper_event['extensions']['extra_fields']['ip'] = current_event['ip']
    caliper_event['extensions']['extra_fields'].update(current_event['context'])
    caliper_event['extensions']['extra_fields'].pop('session')
    return caliper_event
